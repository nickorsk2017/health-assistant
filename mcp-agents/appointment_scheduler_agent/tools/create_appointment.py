import uuid
from datetime import datetime

from loguru import logger
from sqlalchemy import insert, text

from db.engine import SessionLocal
from db.models import Appointment
from schemas.appointment import CreateAppointmentRequest, CreateAppointmentResponse


async def create_appointment(request: CreateAppointmentRequest) -> CreateAppointmentResponse:
    try:
        complaint_id = uuid.UUID(request.complaint_id)
    except ValueError:
        return CreateAppointmentResponse(
            success=False, error=f"Invalid complaint_id: {request.complaint_id}"
        )
    try:
        user_id = uuid.UUID(request.user_id)
    except ValueError:
        return CreateAppointmentResponse(
            success=False, error=f"Invalid user_id: {request.user_id}"
        )

    try:
        appointment_date = datetime.fromisoformat(request.appointment_date)
    except ValueError:
        return CreateAppointmentResponse(
            success=False, error=f"Invalid appointment_date: {request.appointment_date}"
        )

    appointment_id = uuid.uuid4()

    async with SessionLocal() as session:
        await session.execute(
            insert(Appointment).values(
                id=appointment_id,
                complaint_id=complaint_id,
                user_id=user_id,
                appointment_date=appointment_date,
                doctor_type=request.doctor_type,
                problem_notes=request.problem_notes,
            )
        )
        await session.execute(
            text("UPDATE complaints SET status = 'appointment' WHERE id = :complaint_id"),
            {"complaint_id": complaint_id},
        )
        await session.commit()

    logger.info(f"Appointment created: {appointment_id} for complaint {complaint_id}")
    return CreateAppointmentResponse(success=True, appointment_id=str(appointment_id))
