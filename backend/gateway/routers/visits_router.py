from fastapi import APIRouter, HTTPException

from schemas.visit_schema import (
    CreateVisitSchema,
    MutateVisitResponseSchema,
    RecordVisitResponseSchema,
    UpdateVisitSchema,
    VisitsByPromptRequestSchema,
    VisitsByPromptResponseSchema,
)
from services.exceptions import AgentConnectionError, NoDataFoundError
from services.visit_doctor_service import (
    create_visits_by_prompt,
    delete_visit,
    record_visit,
    update_visit,
)

router = APIRouter(prefix="/api/v1/visits", tags=["visits"])


@router.post("", response_model=RecordVisitResponseSchema, status_code=201)
async def create_visit(body: CreateVisitSchema) -> RecordVisitResponseSchema:
    try:
        return await record_visit(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/by-prompt", response_model=VisitsByPromptResponseSchema, status_code=201)
async def create_visits_from_prompt(body: VisitsByPromptRequestSchema) -> VisitsByPromptResponseSchema:
    try:
        return await create_visits_by_prompt(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.patch("/{visit_id}", response_model=MutateVisitResponseSchema)
async def patch_visit(visit_id: str, body: UpdateVisitSchema) -> MutateVisitResponseSchema:
    try:
        return await update_visit(visit_id, body)
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.delete("/{visit_id}", response_model=MutateVisitResponseSchema)
async def remove_visit(visit_id: str) -> MutateVisitResponseSchema:
    try:
        return await delete_visit(visit_id)
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
