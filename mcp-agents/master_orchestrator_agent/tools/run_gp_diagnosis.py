from datetime import timezone

from loguru import logger

from chains.gp_diagnosis_chain import build_gp_diagnosis_chain
from schemas.http import GPDiagnosisRequest, GPDiagnosisResponse
from schemas.state import GPDiagnosisState

_chain = build_gp_diagnosis_chain()


async def run_gp_diagnosis(request: GPDiagnosisRequest) -> GPDiagnosisResponse:
    logger.info(f"Starting GP diagnosis: user={request.user_id}, from={request.start_date}")
    start_date = request.start_date
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    else:
        start_date = start_date.astimezone(timezone.utc)

    initial_state: GPDiagnosisState = {
        "user_id": request.user_id,
        "start_date": start_date.isoformat(),
        "history_records": [],
        "lab_records": [],
        "device_records": [],
        "complaint_records": [],
        "history_error": None,
        "labs_error": None,
        "devices_error": None,
        "complaints_error": None,
        "consilium_findings": [],
        "consultation": {},
        "validation_result": {},
    }

    final_state: GPDiagnosisState = await _chain.ainvoke(initial_state)

    validation = final_state.get("validation_result", {})
    consultation = {
        **final_state["consultation"],
        "validation_percentage": validation.get("validation_score", 0),
        "evidence_citations": validation.get("citations", []),
        "validation_summary": validation.get("summary", ""),
    }

    logger.info(f"GP diagnosis complete for user={request.user_id}")

    return GPDiagnosisResponse(
        consultation=consultation,
        history_available=not bool(final_state["history_error"]),
        labs_available=not bool(final_state["labs_error"]),
        devices_available=not bool(final_state["devices_error"]),
        complaints_available=not bool(final_state["complaints_error"]),
    )
