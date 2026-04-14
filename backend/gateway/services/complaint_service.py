from fastmcp import Client

from config import settings
from schemas.complaint_schema import (
    ComplaintRecordSchema,
    CreateComplaintSchema,
    UpdateComplaintSchema,
)
from services.exceptions import AgentConnectionError, NoDataFoundError


async def create_complaint(data: CreateComplaintSchema) -> ComplaintRecordSchema:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "upsert_complaint",
                {
                    "data": {
                        "user_id": data.user_id,
                        "problem_health": data.problem_health,
                        "date_public": data.date_public,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"complaint_manager_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    if not raw_payload.get("success"):
        raise AgentConnectionError("complaint_manager_agent returned failure on upsert_complaint")

    return await _fetch_single_complaint(raw_payload["complaint_id"])


async def update_complaint(complaint_id: str, data: UpdateComplaintSchema) -> ComplaintRecordSchema:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "upsert_complaint",
                {
                    "data": {
                        "complaint_id": complaint_id,
                        "user_id": data.user_id,
                        "problem_health": data.problem_health,
                        "date_public": data.date_public,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"complaint_manager_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    if not raw_payload.get("success"):
        raise NoDataFoundError(f"Complaint {complaint_id} not found")

    return await _fetch_single_complaint(complaint_id)


async def _fetch_single_complaint(complaint_id: str) -> ComplaintRecordSchema:
    complaints_list = await fetch_complaints("")
    match = next((c for c in complaints_list if c.complaint_id == complaint_id), None)
    if not match:
        raise NoDataFoundError(f"Complaint {complaint_id} not found after upsert")
    return match


async def fetch_complaints(user_id: str) -> list[ComplaintRecordSchema]:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "get_complaints",
                {"data": {"user_id": user_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"complaint_manager_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content
    complaints_list = raw_payload if isinstance(raw_payload, list) else []

    return [ComplaintRecordSchema(**complaint) for complaint in complaints_list]


async def mark_complaint_read(complaint_id: str) -> None:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "mark_as_read",
                {"data": {"complaint_id": complaint_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"complaint_manager_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    if not raw_payload.get("success"):
        raise NoDataFoundError(raw_payload.get("error", f"Complaint {complaint_id} not found"))


async def remove_complaint(complaint_id: str) -> None:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "delete_complaint",
                {"data": {"complaint_id": complaint_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"complaint_manager_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    if not raw_payload.get("success"):
        raise NoDataFoundError(raw_payload.get("error", f"Complaint {complaint_id} not found"))
