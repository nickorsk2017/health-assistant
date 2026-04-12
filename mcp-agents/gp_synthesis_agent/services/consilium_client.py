from fastmcp import Client
from loguru import logger

from config import settings


class ConsiliumClient:
    async def fetch(self, user_id: str, start_date: str) -> list[dict]:
        logger.info(
            f"Connecting to medical-consilium-agent at {settings.consilium_agent_url}"
        )

        async with Client(settings.consilium_agent_url) as client:
            result = await client.call_tool(
                "run_medical_consilium",
                {
                    "data": {
                        "user_id": user_id,
                        "start_date": start_date,
                    }
                },
            )

        payload = result.structured_content or {}
        findings: list[dict] = payload.get("result", [])

        if not isinstance(findings, list):
            logger.error(f"Unexpected consilium response: {result.structured_content}")
            raise TypeError(f"Expected list of findings, got {type(findings)}")

        logger.info(f"Received {len(findings)} specialist finding(s) from consilium")
        return findings
