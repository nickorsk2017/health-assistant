from fastmcp import Client

from config import settings
from schemas.diagnosis_schema import GPConsultationSchema
from services.analysis_service import fetch_analyses
from services.exceptions import AgentConnectionError, NoDataFoundError


async def fetch_gp_consultation(user_id: str, start_date: str) -> GPConsultationSchema:
    try:
        analyses = await fetch_analyses(user_id, start_date)
        analyses_text = [record.analysis for record in analyses]
    except AgentConnectionError as exc:
        raise AgentConnectionError(f"labs_agent unreachable during diagnosis: {exc}") from exc
    except NoDataFoundError:
        analyses_text = []

    try:
        async with Client(settings.gp_synthesis_agent_url) as client:
            response = await client.call_tool(
                "get_final_gp_consultation",
                {
                    "data": {
                        "user_id": user_id,
                        "start_date": start_date,
                        "analyses": analyses_text,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"gp_synthesis_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}

    if not raw_payload:
        raise NoDataFoundError(f"No GP consultation found for user {user_id}")

    return GPConsultationSchema(**raw_payload)
