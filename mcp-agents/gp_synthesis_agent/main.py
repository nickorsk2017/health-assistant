from fastmcp import FastMCP
from loguru import logger

from services.consilium_client import ConsiliumClient
from services.synthesis_service import SynthesisService
from schemas.http import GetSynthesisRequest
from config import settings

logger.add("mcp.log", rotation="10 MB")
mcp = FastMCP("gp-synthesis-agent")

_consilium_client = ConsiliumClient()
_synthesis_service = SynthesisService()


@mcp.resource("config://model")
def get_model() -> str:
    from config import settings
    return f"synthesis_model: {settings.openai_model}"


@mcp.tool(name="get_final_gp_consultation")
async def get_final_gp_consultation(
    data: GetSynthesisRequest
) -> dict:
    """Synthesize multi-specialist consilium findings into a final GP consultation.

    Calls the medical-consilium-agent, routes all specialist findings through a
    senior GP synthesis LLM, and returns a unified diagnosis, treatment plan,
    prognosis, and patient-friendly health narrative.

    Args:
        user_id: Identifier of the patient.
        start_date_clinic_history: ISO 8601 start date for history retrieval (YYYY-MM-DD).
    """
    logger.info(f"GP consultation requested: user={data.user_id}, from={data.start_date}")

    findings = await _consilium_client.fetch(data.user_id, data.start_date)

    if not findings:
        logger.warning(f"No consilium findings returned for user={data.user_id}. Returning advisory response.")
        return {
            "diagnosis": "Insufficient specialist data to establish a unifying diagnosis.",
            "treatment": (
                "Additional specialist consultations and targeted investigations are required "
                "before a treatment plan can be formulated."
            ),
            "prognosis": "Prognosis cannot be assessed without a confirmed diagnosis.",
            "summary": (
                "The medical board reviewed the available clinical data but was unable to identify "
                "a sufficient number of specialist findings to provide a responsible and accurate "
                "consultation. This may be because no visits have been recorded yet, or the history "
                "covers too short a period. Please ensure specialist visits have been recorded in the "
                "system and try again with an earlier start date."
            ),
        }

    consultation = await _synthesis_service.synthesize(findings)

    logger.info(f"GP consultation complete for user={data.user_id}.")
    return consultation.model_dump()


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)

def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
