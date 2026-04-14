
from fastmcp import Client
from loguru import logger

from config import settings


class HistoryClient:
    async def fetch(self, user_id: str, start_date: str) -> list[dict]:
        logger.info(f"Connecting to client_history_agent at {settings.client_history_agent_url}")

        async with Client(settings.client_history_agent_url) as client:
            result = await client.call_tool(
                "get_doctor_visits_history",
                {
                    "data": {
                        "user_id": user_id,
                        "last_date_visit": start_date,
                        "doctor_type": "",
                    }
                },
            )
        payload = result.structured_content or {}
        records = payload.get("result", [])

        if not isinstance(records, list):
            logger.error(f"Unexpected response format: {result.structured_content}")
            raise TypeError(f"Expected list, got {type(records)}: {records}")
        
        logger.info(f"Retrieved {len(records)} SOAP note(s) for user={user_id}")
        return records