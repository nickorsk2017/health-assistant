from datetime import datetime, timezone

from fastmcp import Client

from config import settings
from _common.schemas.diagnosis import DiagnosisResult as GPConsultationSchema
from services.agent_result import AgentResult, to_response


async def fetch_gp_consultation(user_id: str, start_date: datetime) -> AgentResult:
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    else:
        start_date = start_date.astimezone(timezone.utc)
    try:
        async with Client(settings.master_orchestrator_agent_url) as client:
            response = await client.call_tool(
                "run_gp_diagnosis",
                {"data": {"user_id": user_id, "start_date": start_date.isoformat()}},
            )
        raw_results = response.structured_content or {}
        consultation = raw_results.get("consultation", {})
        if not consultation:
            return to_response(error=f"No GP consultation found for user {user_id}")
        return to_response(data=GPConsultationSchema(**consultation))
    except Exception as exc:
        return to_response(error=str(exc))
