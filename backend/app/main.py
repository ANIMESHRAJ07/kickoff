import os

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, check_database_connection, engine
from app.email_service import send_registration_confirmation
from app.models import Registration
from app.schemas import RegistrationCreate, RegistrationResponse

app = FastAPI(title="CodeGenX KICKOFF '26 API")

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
    existing_columns = {column["name"] for column in inspect(engine).get_columns("registrations")}
    with engine.begin() as connection:
        if "email" in existing_columns:
            connection.execute(text("ALTER TABLE registrations MODIFY COLUMN email VARCHAR(255) NULL"))
        if "sap_id" not in existing_columns:
            connection.execute(text("ALTER TABLE registrations ADD COLUMN sap_id VARCHAR(40) NOT NULL DEFAULT ''"))
        if "college" in existing_columns and "branch" not in existing_columns:
            connection.execute(text("ALTER TABLE registrations CHANGE COLUMN college branch VARCHAR(160) NOT NULL"))
        elif "branch" not in existing_columns:
            connection.execute(text("ALTER TABLE registrations ADD COLUMN branch VARCHAR(160) NOT NULL DEFAULT ''"))
        current_columns = {column["name"] for column in inspect(engine).get_columns("registrations")}
        if "whatsapp_same" in current_columns:
            connection.execute(text("ALTER TABLE registrations DROP COLUMN whatsapp_same"))
        current_columns = {column["name"] for column in inspect(engine).get_columns("registrations")}
        if "whatsapp_phone" in current_columns:
            connection.execute(text("ALTER TABLE registrations DROP COLUMN whatsapp_phone"))
        connection.execute(text("UPDATE registrations SET sap_id = CONCAT('LEGACY-', id) WHERE sap_id = '' OR sap_id IS NULL"))
        index_names = {index["name"] for index in inspect(engine).get_indexes("registrations")}
        if "ix_registrations_sap_id" not in index_names:
            connection.execute(text("CREATE UNIQUE INDEX ix_registrations_sap_id ON registrations (sap_id)"))


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome To Kickoff '26"}


@app.get("/db-check")
def db_check():
    try:
        check_database_connection()
        return {"status": "database_connected"}
    except Exception as exc:
        return {
            "status": "database_error",
            "detail": str(exc),
        }


@app.post(
    "/registrations",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_registration(
    registration: RegistrationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_session),
):
    existing_registration = db.scalar(
        select(Registration).where(Registration.sap_id == registration.sap_id)
    )
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A registration already exists for this SAP ID.",
        )

    new_registration = Registration(**registration.model_dump())
    db.add(new_registration)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A registration already exists for this SAP ID.",
        )

    db.refresh(new_registration)
    background_tasks.add_task(
        send_registration_confirmation,
        new_registration.full_name,
        new_registration.sap_id,
        new_registration.branch,
        new_registration.phone,
    )
    return new_registration
