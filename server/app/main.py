

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, create_engine
from app.routers import contacts

from app.settings import CONF
from app.contacts.domain.exceptions import ContactNotFound, EmailAddressNotUnique

logger = logging.getLogger(__name__)


postgre_url = f"postgresql+psycopg2://{CONF.DB_USER}:{CONF.DB_PASSWORD}@{CONF.DB_HOST}:{CONF.DB_PORT}/{CONF.DB_NAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(postgre_url, echo=True)



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(contacts.router)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



@app.exception_handler(RequestValidationError)
async def internal_error_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            {"errors": [{"error": "Internal-error", "message": str(exc)}]}
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"errors": exc.errors()}),
    )


@app.exception_handler(EmailAddressNotUnique)
async def conflict_exception_handler(request: Request, exc: EmailAddressNotUnique):
    return JSONResponse(
        status_code=409,
        content={"errors": [{"error": "Conflict-error", "message": str(exc)}]},
    )


@app.exception_handler(ContactNotFound)
async def not_found_exception_handler(request: Request, exc: ContactNotFound):
    return JSONResponse(
        status_code=404,
        content={"errors": [{"error": "Not-found", "message": str(exc)}]},
    )

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}