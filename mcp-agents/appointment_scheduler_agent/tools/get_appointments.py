from loguru import logger
from sqlalchemy import text

from db.engine import SessionLocal
from db.models import Appointment
from schemas.appointment import AppointmentRecord, GetAppointmentsRequest


async def get_appointments(request: GetAppointmentsRequest) -> list[AppointmentRecord]:
    async with SessionLocal() as session:
        if request.user_id:
            rows = await session.execute(
                text(
                    "SELECT a.id, a.complaint_id, a.user_id, a.appointment_date, "
                    "a.doctor_type, a.problem_notes, a.created_at "
                    "FROM appointments a "
                    "WHERE a.user_id = :user_id "
                    "ORDER BY a.appointment_date ASC"
                ),
                {"user_id": request.user_id},
            )
        else:
            rows = await session.execute(
                text(
                    "SELECT a.id, a.complaint_id, a.user_id, a.appointment_date, "
                    "a.doctor_type, a.problem_notes, a.created_at "
                    "FROM appointments a "
                    "ORDER BY a.appointment_date ASC"
                )
            )
        records = rows.fetchall()

    logger.info(f"Fetched {len(records)} appointment(s) user_filter={request.user_id or 'all'}")
    return [
        AppointmentRecord(
            appointment_id=str(row.id),
            complaint_id=str(row.complaint_id),
            user_id=row.user_id,
            appointment_date=row.appointment_date.isoformat(),
            doctor_type=row.doctor_type,
            problem_notes=row.problem_notes,
            created_at=row.created_at.isoformat(),
        )
        for row in records
    ]
