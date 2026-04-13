import sys
import uuid

from loguru import logger
from sqlalchemy import delete, select

from db.engine import SessionLocal
from db.models import Visit
from schemas.http import DeleteVisitRequest, DeleteVisitResponse

logger.add(sys.stderr, level="INFO")


async def delete_visit(data: DeleteVisitRequest) -> DeleteVisitResponse:
    try:
        visit_id = uuid.UUID(data.visit_id)
    except ValueError:
        msg = f"Invalid visit_id format: {data.visit_id}"
        logger.error(msg)
        return DeleteVisitResponse(success=False, error=msg)

    async with SessionLocal() as session:
        result = await session.execute(select(Visit).where(Visit.id == visit_id))
        if result.scalar_one_or_none() is None:
            msg = f"Visit {visit_id} not found"
            logger.error(msg)
            return DeleteVisitResponse(success=False, error=msg)

        await session.execute(delete(Visit).where(Visit.id == visit_id))
        await session.commit()

    logger.info(f"Visit deleted: {visit_id}")
    return DeleteVisitResponse(success=True)
