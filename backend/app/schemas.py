from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RegistrationCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    sap_id: str = Field(min_length=2, max_length=40)
    phone: str = Field(min_length=7, max_length=30)
    branch: str = Field(min_length=2, max_length=160)
    whatsapp_same: bool = True
    whatsapp_phone: str | None = Field(default=None, min_length=7, max_length=30)

    @model_validator(mode="after")
    def validate_whatsapp(self):
        if not self.whatsapp_same and not self.whatsapp_phone:
            raise ValueError("WhatsApp number is required when it differs from phone")
        return self


class RegistrationResponse(RegistrationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime