from fastapi import APIRouter, HTTPException

from schemas.visit_schema import (
    CreateVisitSchema,
    MutateVisitResponseSchema,
    RecordVisitResponseSchema,
    UpdateVisitSchema,
    VisitsByPromptRequestSchema,
    VisitsByPromptResponseSchema,
)
from services.visit_doctor_service import (
    create_visits_by_prompt,
    delete_visit,
    record_visit,
    update_visit,
)

router = APIRouter(prefix="/api/v1/visits", tags=["visits"])


@router.post("", response_model=RecordVisitResponseSchema, status_code=201)
async def create_visit(body: CreateVisitSchema) -> RecordVisitResponseSchema:
    agent_result = await record_visit(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.post("/by-prompt", response_model=VisitsByPromptResponseSchema, status_code=201)
async def create_visits_from_prompt(body: VisitsByPromptRequestSchema) -> VisitsByPromptResponseSchema:
    agent_result = await create_visits_by_prompt(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.patch("/{visit_id}", response_model=MutateVisitResponseSchema)
async def patch_visit(visit_id: str, body: UpdateVisitSchema) -> MutateVisitResponseSchema:
    agent_result = await update_visit(visit_id, body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.delete("/{visit_id}", response_model=MutateVisitResponseSchema)
async def remove_visit(visit_id: str) -> MutateVisitResponseSchema:
    agent_result = await delete_visit(visit_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]
