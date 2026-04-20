from fastmcp import Client
from loguru import logger

from config import settings
from schemas.state import GPDiagnosisState


async def run_pubmed_validation(state: GPDiagnosisState) -> GPDiagnosisState:
    consultation = state.get("consultation", {})
    keywords = consultation.get("keywords_diagnosis", [])

    if not keywords:
        logger.warning("No diagnosis keywords found — skipping PubMed validation.")
        return {
            **state,
            "validation_result": {
                "validation_score": 0,
                "citations": [],
                "summary": "No diagnosis keywords were provided by the GP synthesis step.",
            },
        }

    logger.info(f"Running PubMed validation for {len(keywords)} keyword(s): {keywords}")

    async with Client(settings.pubmed_validator_agent_url) as client:
        result = await client.call_tool(
            "validate_diagnosis_logic",
            {
                "data": {
                    "keywords_diagnosis": keywords,
                    "clinical_context": {
                        "history_records": state.get("history_records", []),
                        "lab_records": state.get("lab_records", []),
                        "complaint_records": state.get("complaint_records", []),
                        "device_records": state.get("device_records", []),
                    },
                }
            },
        )

    validation = result.structured_content or {}
    logger.info(f"PubMed validation complete: score={validation.get('validation_score', 0)}")
    return {**state, "validation_result": validation}
