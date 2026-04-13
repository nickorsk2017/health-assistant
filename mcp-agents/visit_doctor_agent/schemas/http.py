
from datetime import date

from pydantic import BaseModel, Field
from schemas.visit import DoctorVisit



class RecordDoctorVisitResponse(BaseModel):
    success: bool
    visit_id: str


class GetDoctorVisitsHistoryResponse(BaseModel):
    records: list[DoctorVisit]

class GetDoctorVisitsHistoryRequest(BaseModel):
    last_date_visit: date = Field(description="YYYY-MM-DD, Date of the medical visit in ISO 8601 format (YYYY-MM-DD). Must be today or in the past.", format="date",)
    user_id: str
    doctor_type: str = Field(default="", description="(Optional) Medical specialty to filter visits by. If not provided, returns visits of all specialties.")


class CreateVisitsFromPromptRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    prompt: str = Field(description="Free-text clinical notes describing one or more medical visits.")


class CreateVisitsFromPromptResponse(BaseModel):
    success: bool
    count: int = Field(description="Number of visit records created.")


class UpdateVisitRequest(BaseModel):
    visit_id: str = Field(description="UUID of the visit record to update.")
    visit_at: date = Field(description="ISO 8601 date of the consultation (YYYY-MM-DD).")
    subjective: str = Field(description="Patient complaints, history, and symptoms.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default="", description="Treatment plan or next steps.")


class UpdateVisitResponse(BaseModel):
    success: bool
    error: str = ""


class DeleteVisitRequest(BaseModel):
    visit_id: str = Field(description="UUID of the visit record to delete.")


class DeleteVisitResponse(BaseModel):
    success: bool
    error: str = ""