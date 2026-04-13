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
from services.exceptions import AgentConnectionError, NoDataFoundError


async def record_visit(visit: CreateVisitSchema) -> RecordVisitResponseSchema:
    try:
        async with Client(settings.visit_doctor_agent_url) as client:
            result = await client.call_tool(
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
    except Exception as exc:
        raise AgentConnectionError(f"visit_doctor_agent unreachable: {exc}") from exc

    data = result.structured_content or {}

    if not data:
        raise NoDataFoundError("visit_doctor_agent returned empty result")

    return RecordVisitResponseSchema(success=data.get("success", False), visit_id=data.get("visit_id", ""))


async def fetch_visit_history(user_id: str, last_date_visit: str) -> list[VisitRecordSchema]:
    try:
        async with Client(settings.visit_doctor_agent_url) as client:
            result = await client.call_tool(
                "get_doctor_visits_history",
                {"data": {"user_id": user_id, "last_date_visit": last_date_visit, "doctor_type": ""}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"visit_doctor_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    records = payload.get("result", [])

    if not records:
        raise NoDataFoundError(f"No visit history found for user {user_id}")

    return [VisitRecordSchema(**r) for r in records]


async def create_visits_by_prompt(data: VisitsByPromptRequestSchema) -> VisitsByPromptResponseSchema:
    try:
        async with Client(settings.visit_doctor_agent_url) as client:
            result = await client.call_tool(
                "create_visits_from_prompt",
                {"data": {"user_id": data.user_id, "prompt": data.prompt}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"visit_doctor_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    print("Received response from visit_doctor_agent for prompt processing:", payload)
    response_data = payload.get("result", payload)

    if not response_data:
        raise AgentConnectionError("visit_doctor_agent returned empty result for prompt processing")

    return VisitsByPromptResponseSchema(
        success=response_data.get("success", False),
        count=response_data.get("count", 0),
    )


async def update_visit(visit_id: str, data: UpdateVisitSchema) -> MutateVisitResponseSchema:
    try:
        async with Client(settings.visit_doctor_agent_url) as client:
            result = await client.call_tool(
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
    except Exception as exc:
        raise AgentConnectionError(f"visit_doctor_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    response_data = payload.get("result", payload)

    if not response_data.get("success"):
        raise NoDataFoundError(response_data.get("error", f"Visit {visit_id} not found"))

    return MutateVisitResponseSchema(success=True)


async def delete_visit(visit_id: str) -> MutateVisitResponseSchema:
    try:
        async with Client(settings.visit_doctor_agent_url) as client:
            result = await client.call_tool(
                "delete_visit",
                {"data": {"visit_id": visit_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"visit_doctor_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    response_data = payload.get("result", payload)

    if not response_data.get("success"):
        raise NoDataFoundError(response_data.get("error", f"Visit {visit_id} not found"))

    return MutateVisitResponseSchema(success=True)
