from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP
from loguru import logger

from config import settings
from db.init import create_tables
from schemas.complaint import (
    DeleteComplaintRequest,
    GetComplaintsRequest,
    MarkAsReadRequest,
    UpsertComplaintRequest,
)
from tools.delete_complaint import delete_complaint as _delete_complaint
from tools.get_complaints import get_complaints as _get_complaints
from tools.mark_as_read import mark_as_read as _mark_as_read
from tools.upsert_complaint import upsert_complaint as _upsert_complaint

logger.add("mcp.log", rotation="10 MB")


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    logger.info("Initialising database tables...")
    await create_tables()
    yield


mcp = FastMCP("complaint-manager-agent", lifespan=lifespan)


@mcp.tool(name="upsert_complaint")
async def upsert_complaint(data: UpsertComplaintRequest) -> dict:
    """Create or update a patient complaint.

    Args:
        user_id: ID of the patient submitting the complaint.
        problem_health: Description of the health problem.
        date_public: Date the complaint was reported (ISO format YYYY-MM-DD).
        complaint_id: If provided, updates the existing complaint instead of creating one.
    """
    result = await _upsert_complaint(data)
    return result.model_dump()


@mcp.tool(name="get_complaints")
async def get_complaints(data: GetComplaintsRequest) -> list[dict]:
    """Retrieve complaints for a specific patient.

    Args:
        user_id: Patient UUID used to scope complaints.
    """
    records = await _get_complaints(data)

    return [r.model_dump() for r in records]


@mcp.tool(name="mark_as_read")
async def mark_as_read(data: MarkAsReadRequest) -> dict:
    """Mark a complaint as read by the doctor. No-op if already in 'appointment' status.

    Args:
        complaint_id: UUID of the complaint to mark as read.
    """
    result = await _mark_as_read(data)
    return result.model_dump()


@mcp.tool(name="delete_complaint")
async def delete_complaint(data: DeleteComplaintRequest) -> dict:
    """Permanently delete a complaint.

    Args:
        complaint_id: UUID of the complaint to delete.
    """
    result = await _delete_complaint(data)
    return result.model_dump()


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)


def run_inspector() -> None:
    mcp.run()
