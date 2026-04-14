from pydantic import BaseModel


class CreateAppointmentRequest(BaseModel):
    complaint_id: str
    user_id: str
    appointment_date: str  # ISO format: YYYY-MM-DDTHH:MM:SS
    doctor_type: str
    problem_notes: str = ""


class GetAppointmentsRequest(BaseModel):
    user_id: str = ""  # empty = all (doctor view); filters via complaints JOIN


class AppointmentRecord(BaseModel):
    appointment_id: str
    complaint_id: str
    user_id: str
    appointment_date: str
    doctor_type: str
    problem_notes: str
    created_at: str


class CreateAppointmentResponse(BaseModel):
    success: bool
    appointment_id: str = ""
    error: str = ""
