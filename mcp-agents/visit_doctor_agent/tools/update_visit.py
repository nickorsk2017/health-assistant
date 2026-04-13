import sys
import uuid

from loguru import logger
from sqlalchemy import select, update

from db.engine import SessionLocal
from db.models import Visit
from schemas.http import UpdateVisitRequest, UpdateVisitResponse

logger.add(sys.stderr, level="INFO")


async def update_visit(data: UpdateVisitRequest) -> UpdateVisitResponse:
    try:
        visit_id = uuid.UUID(data.visit_id)
    except ValueError:
        msg = f"Invalid visit_id format: {data.visit_id}"
        logger.error(msg)
        return UpdateVisitResponse(success=False, error=msg)

    async with SessionLocal() as session:
        result = await session.execute(select(Visit).where(Visit.id == visit_id))
        if result.scalar_one_or_none() is None:
            msg = f"Visit {visit_id} not found"
            logger.error(msg)
            return UpdateVisitResponse(success=False, error=msg)

        await session.execute(
            update(Visit)
            .where(Visit.id == visit_id)
            .values(
                visit_at=data.visit_at,
                subjective=data.subjective,
                objective=data.objective,
                assessment=data.assessment,
                plan=data.plan,
            )
        )
        await session.commit()

    logger.info(f"Visit updated: {visit_id}")
    return UpdateVisitResponse(success=True)
