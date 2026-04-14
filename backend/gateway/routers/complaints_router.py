from fastapi import APIRouter, HTTPException, Query

from schemas.complaint_schema import (
    ComplaintRecordSchema,
    CreateComplaintSchema,
    UpdateComplaintSchema,
)
from services.complaint_service import (
    create_complaint,
    fetch_complaints,
    mark_complaint_read,
    remove_complaint,
    update_complaint,
)
from services.exceptions import AgentConnectionError, NoDataFoundError

router = APIRouter(prefix="/api/v1/complaints", tags=["complaints"])


@router.post("", response_model=ComplaintRecordSchema, status_code=201)
async def add_complaint(body: CreateComplaintSchema) -> ComplaintRecordSchema:
    try:
        return await create_complaint(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("", response_model=list[ComplaintRecordSchema])
async def list_complaints(user_id: str = Query(min_length=1)) -> list[ComplaintRecordSchema]:
    try:
        return await fetch_complaints(user_id)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.patch("/{complaint_id}", response_model=ComplaintRecordSchema)
async def edit_complaint(complaint_id: str, body: UpdateComplaintSchema) -> ComplaintRecordSchema:
    try:
        return await update_complaint(complaint_id, body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/{complaint_id}/read", status_code=204)
async def read_complaint(complaint_id: str) -> None:
    try:
        await mark_complaint_read(complaint_id)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.delete("/{complaint_id}", status_code=204)
async def delete_complaint(complaint_id: str) -> None:
    try:
        await remove_complaint(complaint_id)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
