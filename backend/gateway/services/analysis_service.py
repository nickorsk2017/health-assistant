from fastmcp import Client

from config import settings
from schemas.analysis_schema import (
    AnalysisByPromptRequestSchema,
    AnalysisByPromptResponseSchema,
    AnalysisRecordSchema,
    AnalysisRequestSchema,
    AnalysisResponseSchema,
    MutateAnalysisResponseSchema,
    UpdateAnalysisSchema,
)
from services.exceptions import AgentConnectionError, NoDataFoundError


async def record_analysis(data: AnalysisRequestSchema) -> AnalysisResponseSchema:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "add_patient_analysis",
                {
                    "data": {
                        "user_id": data.user_id,
                        "analysis_text": data.analysis_text,
                        "analysis_date": data.analysis_date.isoformat(),
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"labs_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    analysis_data = raw_payload.get("result", raw_payload)

    return AnalysisResponseSchema(success=analysis_data.get("success", False))


async def fetch_analyses(user_id: str, start_date: str) -> list[AnalysisRecordSchema]:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "get_patient_analyses",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"labs_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    analyses_list = raw_payload.get("result", [])

    return [AnalysisRecordSchema(**analysis) for analysis in analyses_list]


async def update_analysis(
    analysis_id: str, data: UpdateAnalysisSchema
) -> MutateAnalysisResponseSchema:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "update_analysis",
                {
                    "data": {
                        "analysis_id": analysis_id,
                        "analysis_text": data.analysis_text,
                        "analysis_date": data.analysis_date,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"labs_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    analysis_data = raw_payload.get("result", raw_payload)

    if not analysis_data.get("success"):
        raise NoDataFoundError(analysis_data.get("error", f"Analysis {analysis_id} not found"))

    return MutateAnalysisResponseSchema(success=True)


async def delete_analysis(analysis_id: str) -> MutateAnalysisResponseSchema:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "delete_analysis",
                {"data": {"analysis_id": analysis_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"labs_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    analysis_data = raw_payload.get("result", raw_payload)

    if not analysis_data.get("success"):
        raise NoDataFoundError(analysis_data.get("error", f"Analysis {analysis_id} not found"))

    return MutateAnalysisResponseSchema(success=True)


async def create_analyses_from_prompt(
    data: AnalysisByPromptRequestSchema,
) -> AnalysisByPromptResponseSchema:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "create_analyses_from_prompt",
                {"data": {"user_id": data.user_id, "prompt": data.prompt}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"labs_agent unreachable: {exc}") from exc

    raw_payload = response.structured_content or {}
    analysis_data = raw_payload.get("result", raw_payload)

    return AnalysisByPromptResponseSchema(
        success=analysis_data.get("success", False),
        list_missing_analysis=analysis_data.get("list_missing_analysis", []),
    )
