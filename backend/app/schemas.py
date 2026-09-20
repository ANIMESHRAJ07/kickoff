from datetime import datetime

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RegistrationCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    sap_id: str = Field(min_length=2, max_length=40)
    phone: str = Field(min_length=7, max_length=30)
    branch: str = Field(min_length=2, max_length=160)
    study_year: Literal["1st Year", "2nd Year", "3rd Year"]


class RegistrationResponse(RegistrationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime