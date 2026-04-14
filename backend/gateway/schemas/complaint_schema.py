from typing import Literal

from pydantic import BaseModel

ComplaintStatus = Literal["unread", "read", "appointment"]


class CreateComplaintSchema(BaseModel):
    user_id: str
    problem_health: str
    date_public: str


class UpdateComplaintSchema(BaseModel):
    user_id: str
    problem_health: str
    date_public: str


class ComplaintRecordSchema(BaseModel):
    complaint_id: str
    user_id: str
    problem_health: str
    date_public: str
    status: ComplaintStatus
    created_at: str
