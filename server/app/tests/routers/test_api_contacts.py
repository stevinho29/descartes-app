import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.routers.contacts import get_session
from app.contacts.adapters.contact_database import Contact

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def setup_contacts(session:Session):
    contacts = [Contact(**{"first_name": "steve", "last_name": "Ndemanou", "email": "steve.ndemanou@test.com", "job": "factor", "comment": "first comment"}),
                Contact(**{"first_name": "jérémie", "last_name": "Duchemin", "email": "jérémie.duchemin@test.com", "job": "developer", "comment": "second comment"}),
                Contact(**{"first_name": "itoshi", "last_name": "Sae", "email": "itoshi.sae@test.com", "job": "assistant", "comment": "third comment"})]
    session.add_all(contacts)
    session.commit()
    
def assert_well_formed(contact:dict):
    assert contact.get("email") is not None
    assert contact.get("first_name") is not None
    assert contact.get("last_name") is not None
    assert contact.get("job") is not None
    assert contact.get("comment") is not None

def test_get_contacts_ok(client: TestClient, session:Session):
    setup_contacts(session=session)

    response = client.get(url="/contacts",
                          params={})
    assert response.status_code == 200
    assert response.json().get("total") == 3
    data = response.json().get("data")

    for contact in data:
        assert_well_formed(contact)
    
    # range
    response = client.get(url="/contacts",
                          params={"range": "0-1"})
    assert response.status_code == 206
    data = response.json().get("data")
    assert len(data) == 1

    # only
    response = client.get(url="/contacts",
                          params={"only": ["email"]})
    assert response.status_code == 200
    assert response.json().get("total") == 3

    # sort, desc
    response = client.get(url="/contacts",
                          params={"sort": ["first_name"]})
    assert response.status_code == 200
    assert response.json().get("total") == 3
    data = response.json().get("data")
    assert data[0].get("first_name") == "itoshi"
    assert data[1].get("first_name") == "jérémie"
    assert data[2].get("first_name") == "steve"

def test_get_contacts_validation_error(client:TestClient):
    # bad range
    response = client.get(url="/contacts",
                          params={"range": "-100-1"})
    assert response.status_code == 400
    # unknown field for sort, desc, only
    response = client.get(url="/contacts",
                          params={"sort": ["unknown"]})
    assert response.status_code == 400

    response = client.get(url="/contacts",
                          params={"desc": ["unknown"]})
    assert response.status_code == 400

def test_get_contacts_not_found(client: TestClient):
    response = client.get(url="/contacts",
                          params={})
    assert response.status_code == 404
    assert response.json().get("errors") is not None