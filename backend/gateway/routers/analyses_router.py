from fastapi import APIRouter, HTTPException, Query

from schemas.analysis_schema import (
    AnalysisByPromptRequestSchema,
    AnalysisByPromptResponseSchema,
    AnalysisRecordSchema,
    AnalysisRequestSchema,
    AnalysisResponseSchema,
    MutateAnalysisResponseSchema,
    UpdateAnalysisSchema,
)
from services.analysis_service import (
    create_analyses_from_prompt,
    delete_analysis,
    fetch_analyses,
    record_analysis,
    update_analysis,
)

router = APIRouter(prefix="/api/v1/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResponseSchema, status_code=201)
async def add_analysis(body: AnalysisRequestSchema) -> AnalysisResponseSchema:
    agent_result = await record_analysis(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.post("/by-prompt", response_model=AnalysisByPromptResponseSchema, status_code=201)
async def import_analyses_from_prompt(body: AnalysisByPromptRequestSchema) -> AnalysisByPromptResponseSchema:
    agent_result = await create_analyses_from_prompt(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.patch("/{analysis_id}", response_model=MutateAnalysisResponseSchema)
async def patch_analysis(analysis_id: str, body: UpdateAnalysisSchema) -> MutateAnalysisResponseSchema:
    agent_result = await update_analysis(analysis_id, body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.delete("/{analysis_id}", response_model=MutateAnalysisResponseSchema)
async def remove_analysis(analysis_id: str) -> MutateAnalysisResponseSchema:
    agent_result = await delete_analysis(analysis_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.get("/{user_id}", response_model=list[AnalysisRecordSchema])
async def get_analyses(
    user_id: str,
    start_date: str = Query(
        default="2000-01-01",
        description="ISO 8601 start date (YYYY-MM-DD). Returns all analyses from this date onward.",
    ),
) -> list[AnalysisRecordSchema]:
    agent_result = await fetch_analyses(user_id, start_date)
    if not agent_result["success"]:
        return []
    return agent_result["data"]
