
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List


class RecipientInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class JobCreate(BaseModel):
    event_name: str = Field(min_length=2, max_length=150)
    certificate_title: str = Field(min_length=2, max_length=150)
    recipients: List[RecipientInput] = Field(min_length=1, max_length=500)


class CertificateResponse(BaseModel):
    id: int
    recipient_name: str
    recipient_email: str
    status: str
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class JobResponse(BaseModel):
    id: int
    event_name: str
    certificate_title: str
    status: str
    total: int
    successful: int
    failed: int

    model_config = ConfigDict(from_attributes=True)
