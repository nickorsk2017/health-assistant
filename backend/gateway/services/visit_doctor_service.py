from fastmcp import Client

from config import settings
from schemas.visit_schema import (
    CreateVisitSchema,
    MutateVisitResponseSchema,
    RecordVisitResponseSchema,
    UpdateVisitSchema,
    VisitRecordSchema,
    VisitsByPromptRequestSchema,
    VisitsByPromptResponseSchema,
)
from services.agent_result import AgentResult


async def record_visit(visit: CreateVisitSchema) -> AgentResult:
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "add_visit_doctor",
                {
                    "data": {
                        "user_id": visit.user_id,
                        "doctor_type": visit.doctor_type.value,
                        "visit_at": visit.visit_at,
                        "subjective": visit.subjective,
                        "objective": visit.objective,
                        "assessment": visit.assessment,
                        "plan": visit.plan,
                    }
                },
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": "client_history_agent returned failure on add_visit_doctor"}
        return {
            "success": True,
            "data": RecordVisitResponseSchema(
                success=True,
                visit_id=raw_results.get("visit_id", ""),
            ),
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def fetch_visit_history(user_id: str, last_date_visit: str) -> AgentResult:
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "get_doctor_visits_history",
                {"data": {"user_id": user_id, "last_date_visit": last_date_visit, "doctor_type": ""}},
            )
        raw_results = response.structured_content or {}
        visits_collection = raw_results.get("result", [])
        return {
            "success": True,
            "data": [VisitRecordSchema(**visit) for visit in visits_collection],
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": [], "error": str(exc)}


async def create_visits_by_prompt(data: VisitsByPromptRequestSchema) -> AgentResult:
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "create_visits_from_prompt",
                {"data": {"user_id": data.user_id, "prompt": data.prompt}},
            )
        raw_results = response.structured_content or {}
        visits_data = raw_results.get("result", raw_results)
        return {
            "success": True,
            "data": VisitsByPromptResponseSchema(
                success=visits_data.get("success", False),
                count=visits_data.get("count", 0),
            ),
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def update_visit(visit_id: str, data: UpdateVisitSchema) -> AgentResult:
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "update_visit",
                {
                    "data": {
                        "visit_id": visit_id,
                        "visit_at": data.visit_at,
                        "subjective": data.subjective,
                        "objective": data.objective,
                        "assessment": data.assessment,
                        "plan": data.plan,
                    }
                },
            )
        raw_results = response.structured_content or {}
        visit_data = raw_results.get("result", raw_results)
        if not visit_data.get("success"):
            return {"success": False, "data": None, "error": visit_data.get("error", f"Visit {visit_id} not found")}
        return {"success": True, "data": MutateVisitResponseSchema(success=True), "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def delete_visit(visit_id: str) -> AgentResult:
    try:
        async with Client(settings.client_history_agent_url) as client:
            response = await client.call_tool(
                "delete_visit",
                {"data": {"visit_id": visit_id}},
            )
        raw_results = response.structured_content or {}
        visit_data = raw_results.get("result", raw_results)
        if not visit_data.get("success"):
            return {"success": False, "data": None, "error": visit_data.get("error", f"Visit {visit_id} not found")}
        return {"success": True, "data": MutateVisitResponseSchema(success=True), "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}
