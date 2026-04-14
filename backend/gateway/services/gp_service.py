from fastmcp import Client

from config import settings
from schemas.diagnosis_schema import GPConsultationSchema
from services.agent_result import AgentResult
from services.analysis_service import fetch_analyses


async def fetch_gp_consultation(user_id: str, start_date: str) -> AgentResult:
    analyses_result = await fetch_analyses(user_id, start_date)
    analyses_text = (
        [record.analysis for record in analyses_result["data"]]
        if analyses_result["success"]
        else []
    )

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
        raw_results = response.structured_content or {}
        if not raw_results:
            return {"success": False, "data": None, "error": f"No GP consultation found for user {user_id}"}
        return {"success": True, "data": GPConsultationSchema(**raw_results), "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}
