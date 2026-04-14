from fastmcp import Client

from config import settings
from schemas.consilium_schema import SpecialistFindingSchema
from services.exceptions import AgentConnectionError, NoDataFoundError


async def fetch_consilium(user_id: str, start_date: str) -> list[SpecialistFindingSchema]:
    try:
        async with Client(settings.doctors_agent_url) as client:
            response = await client.call_tool(
                "run_medical_consilium",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"doctors_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    findings_list = raw_payload.get("result", [])

    if not findings_list:
        raise NoDataFoundError(f"No consilium findings for user {user_id}")

    return [SpecialistFindingSchema(**finding) for finding in findings_list]
