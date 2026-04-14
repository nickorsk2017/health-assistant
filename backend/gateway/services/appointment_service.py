from fastmcp import Client

from config import settings
from schemas.appointment_schema import AppointmentRecordSchema, CreateAppointmentSchema
from services.agent_result import AgentResult


async def create_appointment(data: CreateAppointmentSchema) -> AgentResult:
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
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": raw_results.get("error", "appointment_scheduler_agent returned failure")}

        fetch_result = await fetch_appointments(data.user_id)
        if not fetch_result["success"]:
            return fetch_result
        appointment = next(
            (a for a in fetch_result["data"] if a.appointment_id == raw_results["appointment_id"]),
            None,
        )
        if not appointment:
            return {"success": False, "data": None, "error": "Appointment created but could not be retrieved"}
        return {"success": True, "data": appointment, "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def fetch_appointments(user_id: str) -> AgentResult:
    try:
        async with Client(settings.appointment_scheduler_agent_url) as client:
            response = await client.call_tool(
                "get_appointments",
                {"data": {"user_id": user_id}},
            )
        raw_results = response.structured_content
        appointments_collection = raw_results if isinstance(raw_results, list) else []
        return {
            "success": True,
            "data": [AppointmentRecordSchema(**appointment) for appointment in appointments_collection],
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": [], "error": str(exc)}
