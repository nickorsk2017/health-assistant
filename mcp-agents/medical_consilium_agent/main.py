from fastmcp import FastMCP
from loguru import logger

from services.consilium_service import ConsiliumService
from services.history_client import HistoryClient
from schemas.http import GetDoctorVisitsHistoryRequest
from config import settings

logger.add("mcp.log", rotation="10 MB")

mcp = FastMCP("medical-consilium-agent")

_history_client = HistoryClient()
_consilium_service = ConsiliumService()


@mcp.resource("config://specialties")
def get_specialties() -> str:
    return (
        "specialties: oncology, gastroenterology, cardiology, hematology, "
        "nephrology, nutrition, endocrinology, mental_health, pulmonology"
    )


@mcp.tool(name="run_medical_consilium")
async def run_medical_consilium(data: GetDoctorVisitsHistoryRequest) -> list[dict]:
    """Run a patient's full medical history through a board of 9 specialist LLMs in parallel.

    Args:
        user_id: Identifier of the patient.
        start_date_clinic_history: ISO 8601 start date for history retrieval (YYYY-MM-DD).
    """
    logger.info(f"Starting consilium: user={data.user_id}, from={data.start_date}")

    records = await _history_client.fetch(data.user_id, data.start_date)
    findings = await _consilium_service.run(records)

    logger.info(f"Consilium finished: {len(findings)} specialist finding(s) returned.")
    return [f.model_dump() for f in findings]


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)

if __name__ == "__main__":
    run()
