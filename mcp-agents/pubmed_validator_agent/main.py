from fastmcp import FastMCP
from loguru import logger

from config import settings
from schemas.http import ValidationRequest
from services.validation_service import ValidationService

logger.add("mcp.log", rotation="10 MB")

mcp = FastMCP("pubmed-validator-agent")

_validation_service = ValidationService()


@mcp.tool(name="validate_diagnosis_logic")
async def validate_diagnosis_logic(data: ValidationRequest) -> dict:
    """Validate an AI diagnosis against real-world PubMed medical literature.

    Searches PubMed for clinical correlations between the proposed diagnosis
    keywords and the patient's symptoms, labs, and complaints. Returns an
    evidence-based validation score, supporting citations, and a scientific summary.

    Args:
        keywords_diagnosis: Medical keyword variants of the suspected diagnosis.
        clinical_context: Patient history, labs, complaints, and device data.
    """
    logger.info(
        f"Validation requested: {len(data.keywords_diagnosis)} keyword(s), "
        f"{len(data.clinical_context.history_records)} history record(s)"
    )

    result = await _validation_service.validate(
        keywords=data.keywords_diagnosis,
        clinical_context=data.clinical_context,
    )

    logger.info(f"Validation done: score={result.validation_score}")
    return result.model_dump()


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
