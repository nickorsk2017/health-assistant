from pydantic import BaseModel


class CreateAppointmentSchema(BaseModel):
    complaint_id: str
    user_id: str
    appointment_date: str
    doctor_type: str
    problem_notes: str = ""


class AppointmentRecordSchema(BaseModel):
    appointment_id: str
    complaint_id: str
    user_id: str
    appointment_date: str
    doctor_type: str
    problem_notes: str
    created_at: str
