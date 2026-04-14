from fastmcp import Client

from config import settings
from schemas.appointment_schema import AppointmentRecordSchema, CreateAppointmentSchema
from services.exceptions import AgentConnectionError


async def create_appointment(data: CreateAppointmentSchema) -> AppointmentRecordSchema:
    try:
        async with Client(settings.appointment_scheduler_agent_url) as client:
            response = await client.call_tool(
                "create_appointment",
                {
                    "data": {
                        "complaint_id": data.complaint_id,
                        "user_id": data.user_id,
                        "appointment_date": data.appointment_date,
                        "doctor_type": data.doctor_type,
                        "problem_notes": data.problem_notes,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"appointment_scheduler_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    if not raw_payload.get("success"):
        raise AgentConnectionError(
            raw_payload.get("error", "appointment_scheduler_agent returned failure")
        )

    appointments_list = await fetch_appointments(data.user_id)
    appointment = next(
        (a for a in appointments_list if a.appointment_id == raw_payload["appointment_id"]),
        None,
    )
    if not appointment:
        raise AgentConnectionError("Appointment created but could not be retrieved")
    return appointment


async def fetch_appointments(user_id: str) -> list[AppointmentRecordSchema]:
    try:
        async with Client(settings.appointment_scheduler_agent_url) as client:
            response = await client.call_tool(
                "get_appointments",
                {"data": {"user_id": user_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"appointment_scheduler_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content
    appointments_list = raw_payload if isinstance(raw_payload, list) else []

    return [AppointmentRecordSchema(**appointment) for appointment in appointments_list]
