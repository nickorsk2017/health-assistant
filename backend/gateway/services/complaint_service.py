from fastmcp import Client

from config import settings
from schemas.complaint_schema import (
    ComplaintRecordSchema,
    CreateComplaintSchema,
    UpdateComplaintSchema,
)
from services.agent_result import AgentResult


async def create_complaint(data: CreateComplaintSchema) -> AgentResult:
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
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": "complaint_manager_agent returned failure on upsert_complaint"}

        complaint_id = raw_results["complaint_id"]
        fetch_result = await fetch_complaints("")
        if not fetch_result["success"]:
            return fetch_result
        complaint = next((c for c in fetch_result["data"] if c.complaint_id == complaint_id), None)
        if not complaint:
            return {"success": False, "data": None, "error": f"Complaint {complaint_id} not found after create"}
        return {"success": True, "data": complaint, "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def update_complaint(complaint_id: str, data: UpdateComplaintSchema) -> AgentResult:
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
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": f"Complaint {complaint_id} not found"}

        fetch_result = await fetch_complaints("")
        if not fetch_result["success"]:
            return fetch_result
        complaint = next((c for c in fetch_result["data"] if c.complaint_id == complaint_id), None)
        if not complaint:
            return {"success": False, "data": None, "error": f"Complaint {complaint_id} not found after update"}
        return {"success": True, "data": complaint, "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def fetch_complaints(user_id: str) -> AgentResult:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "get_complaints",
                {"data": {"user_id": user_id}},
            )
        raw_results = response.structured_content
        complaints_collection = raw_results if isinstance(raw_results, list) else []
        return {
            "success": True,
            "data": [ComplaintRecordSchema(**complaint) for complaint in complaints_collection],
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": [], "error": str(exc)}


async def mark_complaint_read(complaint_id: str) -> AgentResult:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "mark_as_read",
                {"data": {"complaint_id": complaint_id}},
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": raw_results.get("error", f"Complaint {complaint_id} not found")}
        return {"success": True, "data": None, "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def remove_complaint(complaint_id: str) -> AgentResult:
    try:
        async with Client(settings.complaint_manager_agent_url) as client:
            response = await client.call_tool(
                "delete_complaint",
                {"data": {"complaint_id": complaint_id}},
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": raw_results.get("error", f"Complaint {complaint_id} not found")}
        return {"success": True, "data": None, "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}
