from fastmcp import Client

from config import settings
from schemas.consilium_schema import SpecialistFindingSchema
from services.agent_result import AgentResult


async def fetch_consilium(user_id: str, start_date: str) -> AgentResult:
    try:
        async with Client(settings.doctors_agent_url) as client:
            response = await client.call_tool(
                "run_medical_consilium",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
        raw_results = response.structured_content or {}
        findings_collection = raw_results.get("result", [])
        if not findings_collection:
            return {"success": False, "data": [], "error": f"No consilium findings for user {user_id}"}
        return {
            "success": True,
            "data": [SpecialistFindingSchema(**finding) for finding in findings_collection],
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": [], "error": str(exc)}
