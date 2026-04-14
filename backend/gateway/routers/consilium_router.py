from fastapi import APIRouter, HTTPException, Query

from schemas.consilium_schema import SpecialistFindingSchema
from services.consilium_service import fetch_consilium

router = APIRouter(prefix="/api/v1/consilium", tags=["consilium"])


@router.get("/{user_id}", response_model=list[SpecialistFindingSchema])
async def get_consilium(
    user_id: str,
    start_date: str = Query(description="ISO 8601 date (YYYY-MM-DD). Analyse visits from this date onward."),
) -> list[SpecialistFindingSchema]:
    agent_result = await fetch_consilium(user_id, start_date)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]
