from fastapi import APIRouter, HTTPException, Query

from schemas.visit_schema import VisitRecordSchema
from services.visit_doctor_service import fetch_visit_history

router = APIRouter(prefix="/api/v1/history", tags=["history"])


@router.get("/{user_id}", response_model=list[VisitRecordSchema])
async def get_history(
    user_id: str,
    last_date_visit: str = Query(description="ISO 8601 date (YYYY-MM-DD). Returns visits from this date onward."),
) -> list[VisitRecordSchema]:
    agent_result = await fetch_visit_history(user_id, last_date_visit)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]
