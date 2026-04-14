import uuid
from datetime import date, datetime

from pydantic import BaseModel


class CreatePatientSchema(BaseModel):
    full_name: str
    dob: date
    gender: str
    email: str | None = None


class PatientSchema(BaseModel):
    id: uuid.UUID
    full_name: str
    dob: date
    gender: str
    email: str | None = None
    created_at: datetime
