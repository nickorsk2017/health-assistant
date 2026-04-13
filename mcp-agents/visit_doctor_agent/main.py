from contextlib import asynccontextmanager
from datetime import date
from typing import AsyncIterator

from fastmcp import FastMCP
from loguru import logger

from config import settings
from db.init import create_tables
from schemas.visit import DoctorVisit
from schemas.http import (
    CreateVisitsFromPromptRequest,
    DeleteVisitRequest,
    GetDoctorVisitsHistoryRequest,
    UpdateVisitRequest,
)
from tools.add_visit_doctor import add_visit_doctor as _record_visit
from tools.create_visits_from_prompt import create_visits_from_prompt as _create_from_prompt
from tools.delete_visit import delete_visit as _delete_visit
from tools.get_doctor_visits_history import get_doctor_visits_history as _get_history
from tools.update_visit import update_visit as _update_visit

logger.add("mcp.log", rotation="10 MB")

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    logger.info("Initialising database tables...")
    await create_tables()
    logger.info("Database ready.")
    yield


mcp = FastMCP("visit-doctor-mcp-agent", lifespan=lifespan)


@mcp.resource("config://schema")
def get_schema() -> str:
    return (
        "table: visits\n"
        "columns: id (uuid), user_id, doctor_type, visit_at, "
        "subjective, objective, assessment, plan, created_at"
    )


@mcp.tool(name="add_visit_doctor")
async def add_visit_doctor(data: DoctorVisit) -> dict:
    """Record a new specialist consultation in SOAP format.

    Args:
        doctor_type: Medical specialty (oncology, gastroenterology, cardiology,
            hematology, nephrology, nutrition, endocrinology, mental_health, pulmonology).
        subjective: Patient complaints, history, and symptoms as reported.
        objective: Clinical findings, vitals, and examination results.
        assessment: Clinical impression or diagnosis.
        visit_at: ISO 8601 date of the consultation (YYYY-MM-DD).
        user_id: Identifier of the patient.
        plan: Treatment plan or next steps (optional).
    """
    result = await _record_visit(data)
    return result.model_dump()


@mcp.tool(name="get_doctor_visits_history")
async def get_doctor_visits_history(
    data: GetDoctorVisitsHistoryRequest
) -> list[DoctorVisit]:
    """Retrieve SOAP notes for a user from a given date to today.

    Args:
        last_date_visit: ISO 8601 start date for the search (YYYY-MM-DD).
        user_id: Identifier of the patient.
        doctor_type: Optional specialty filter (oncology, gastroenterology, cardiology,
            hematology, nephrology, nutrition, endocrinology, mental_health, pulmonology).
    """
    records = await _get_history(data)
    return [r.model_dump() for r in records]


@mcp.tool(name="create_visits_from_prompt")
async def create_visits_from_prompt(data: CreateVisitsFromPromptRequest) -> dict:
    """Parse a natural language prompt and batch-create multiple SOAP visit records.

    Args:
        user_id: Identifier of the patient.
        prompt: Free-text clinical notes describing one or more medical visits. May include
            dates, specialist types, symptoms, findings, diagnoses, and treatment plans.
            Multiple visits on different dates are supported in a single prompt.
    """
    result = await _create_from_prompt(data)
    return result.model_dump()


@mcp.tool(name="update_visit")
async def update_visit(data: UpdateVisitRequest) -> dict:
    """Update an existing SOAP visit record.

    Args:
        visit_id: UUID of the visit record to update.
        visit_at: ISO 8601 date of the consultation (YYYY-MM-DD).
        subjective: Patient complaints, history, and symptoms.
        objective: Clinical findings, vitals, and examination results.
        assessment: Clinical impression or diagnosis.
        plan: Treatment plan or next steps.
    """
    result = await _update_visit(data)
    return result.model_dump()


@mcp.tool(name="delete_visit")
async def delete_visit(data: DeleteVisitRequest) -> dict:
    """Permanently delete a visit record by its ID.

    Args:
        visit_id: UUID of the visit record to delete.
    """
    result = await _delete_visit(data)
    return result.model_dump()


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)

def run_inspector() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
