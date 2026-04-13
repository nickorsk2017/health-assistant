from enum import Enum

from pydantic import BaseModel, Field


class DoctorTypeSchema(str, Enum):
    oncology = "oncology"
    gastroenterology = "gastroenterology"
    cardiology = "cardiology"
    hematology = "hematology"
    nephrology = "nephrology"
    nutrition = "nutrition"
    endocrinology = "endocrinology"
    mental_health = "mental_health"
    pulmonology = "pulmonology"
    general_practitioner = "general_practitioner"


class CreateVisitSchema(BaseModel):
    user_id: str = Field(description="Patient identifier.")
    doctor_type: DoctorTypeSchema
    visit_at: str = Field(description="ISO 8601 date of the consultation (YYYY-MM-DD).")
    subjective: str = Field(description="Patient complaints, history, and symptoms.")
    objective: str = Field(description="Clinical findings, vitals, and examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(default="", description="Treatment plan or next steps.")


class RecordVisitResponseSchema(BaseModel):
    success: bool
    visit_id: str


class VisitRecordSchema(BaseModel):
    visit_id: str
    user_id: str
    doctor_type: str
    visit_at: str
    subjective: str
    objective: str
    assessment: str
    plan: str = ""
    created_at: str = ""


class VisitsByPromptRequestSchema(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    prompt: str = Field(description="Free-text clinical notes to be parsed into SOAP visits.")


class VisitsByPromptResponseSchema(BaseModel):
    success: bool
    count: int = Field(description="Number of visit records created.")


class UpdateVisitSchema(BaseModel):
    visit_at: str = Field(description="ISO 8601 date of the consultation (YYYY-MM-DD).")
    subjective: str
    objective: str
    assessment: str
    plan: str = ""


class MutateVisitResponseSchema(BaseModel):
    success: bool
