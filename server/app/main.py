


from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, create_engine
from app.routers import contacts

from app.settings import CONF
from app.contacts.domain.exceptions import ContactNotFound, EmailAddressNotUnique

postgre_url = f"postgresql+psycopg2://{CONF.DB_USER}:{CONF.DB_PASSWORD}@{CONF.DB_HOST}:{CONF.DB_PORT}/{CONF.DB_NAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(postgre_url, echo=True)

app = FastAPI()
app.include_router(contacts.router)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



@app.exception_handler(RequestValidationError)
async def internal_error_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {"errors": [{"error": "Internal-error", "message": str(exc)}]}
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"errors": exc.errors()}),
    )


@app.exception_handler(EmailAddressNotUnique)
async def conflict_exception_handler(request: Request, exc: EmailAddressNotUnique):
    return JSONResponse(
        status_code=418,
        content={"errors": [{"error": "Conflict-error", "message": str(exc)}]},
    )


@app.exception_handler(ContactNotFound)
async def not_found_exception_handler(request: Request, exc: ContactNotFound):
    return JSONResponse(
        status_code=404,
        content={"errors": [{"error": "Not-found", "message": str(exc)}]},
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


