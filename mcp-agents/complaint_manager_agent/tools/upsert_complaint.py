import uuid
from datetime import date

from loguru import logger
from sqlalchemy import insert, select, update

from db.engine import SessionLocal
from db.models import Complaint, COMPLAINT_STATUS_UNREAD
from schemas.complaint import ComplaintRecord, UpsertComplaintRequest, UpsertComplaintResponse


def to_record(row: Complaint) -> ComplaintRecord:
    return ComplaintRecord(
        complaint_id=str(row.id),
        user_id=row.user_id,
        problem_health=row.problem_health,
        date_public=row.date_public.isoformat(),
        status=row.status,
        created_at=row.created_at.isoformat(),
    )


async def upsert_complaint(request: UpsertComplaintRequest) -> UpsertComplaintResponse:
    date_public = date.fromisoformat(request.date_public)

    if request.complaint_id:
        complaint_id = uuid.UUID(request.complaint_id)
        async with SessionLocal() as session:
            result = await session.execute(select(Complaint).where(Complaint.id == complaint_id))
            existing = result.scalar_one_or_none()
            if existing is None:
                return UpsertComplaintResponse(success=False, complaint_id="")
            await session.execute(
                update(Complaint)
                .where(Complaint.id == complaint_id)
                .values(problem_health=request.problem_health, date_public=date_public)
            )
            await session.commit()
            refreshed = await session.execute(select(Complaint).where(Complaint.id == complaint_id))
            updated = refreshed.scalar_one()
        logger.info(f"Complaint updated: {complaint_id}")
        return UpsertComplaintResponse(
            success=True,
            complaint_id=str(complaint_id),
            complaint=to_record(updated),
        )

    complaint_id = uuid.uuid4()
    async with SessionLocal() as session:
        await session.execute(
            insert(Complaint).values(
                id=complaint_id,
                user_id=request.user_id,
                problem_health=request.problem_health,
                date_public=date_public,
                status=COMPLAINT_STATUS_UNREAD,
            )
        )
        await session.commit()
        created = await session.execute(select(Complaint).where(Complaint.id == complaint_id))
        row = created.scalar_one()

    logger.info(f"Complaint created: {complaint_id} for user {request.user_id}")
    return UpsertComplaintResponse(
        success=True,
        complaint_id=str(complaint_id),
        complaint=to_record(row),
    )
