from loguru import logger
from sqlalchemy import select

from db.engine import SessionLocal
from db.models import Complaint
from schemas.complaint import ComplaintRecord, GetComplaintsRequest


async def get_complaints(request: GetComplaintsRequest) -> list[ComplaintRecord]:
    query = (
        select(Complaint)
        .where(Complaint.user_id == request.user_id)
        .order_by(Complaint.created_at.desc())
    )

    async with SessionLocal() as session:
        result = await session.execute(query)
        rows = result.scalars().all()

    logger.info(f"Fetched {len(rows)} complaint(s) user_filter={request.user_id}")
    return [
        ComplaintRecord(
            complaint_id=str(row.id),
            user_id=row.user_id,
            problem_health=row.problem_health,
            date_public=row.date_public.isoformat(),
            status=row.status,
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]
