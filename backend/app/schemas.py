from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RegistrationCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    sap_id: str = Field(min_length=2, max_length=40)
    phone: str = Field(min_length=7, max_length=30)
    branch: str = Field(min_length=2, max_length=160)


class RegistrationResponse(RegistrationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime