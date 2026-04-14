from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

ComplaintStatus = Literal["unread", "read", "appointment"]


class UpsertComplaintRequest(BaseModel):
    user_id: str = Field(description="UUID of the patient submitting the complaint.")
    problem_health: str = Field(description="Description of the symptom or health problem.")
    date_public: str = Field(description="ISO 8601 date when the patient started feeling this (YYYY-MM-DD).")
    complaint_id: str | None = Field(
        default=None,
        description="UUID of an existing complaint to update. Omit to create a new one.",
    )


class UpsertComplaintResponse(BaseModel):
    success: bool
    complaint_id: str
    complaint: "ComplaintRecord | None" = None


class GetComplaintsRequest(BaseModel):
    user_id: str = Field(
        min_length=1,
        description="Patient UUID to filter complaints by.",
    )


class ComplaintRecord(BaseModel):
    complaint_id: str
    user_id: str
    problem_health: str
    date_public: str
    status: ComplaintStatus
    created_at: str


class MarkAsReadRequest(BaseModel):
    complaint_id: str = Field(description="UUID of the complaint to mark as read.")


class MutateComplaintResponse(BaseModel):
    success: bool
    error: str = ""


class DeleteComplaintRequest(BaseModel):
    complaint_id: str = Field(description="UUID of the complaint to delete.")


UpsertComplaintResponse.model_rebuild()
