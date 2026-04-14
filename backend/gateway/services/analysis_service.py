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
from services.agent_result import AgentResult


async def record_analysis(data: AnalysisRequestSchema) -> AgentResult:
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
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        return {
            "success": True,
            "data": AnalysisResponseSchema(success=analysis_data.get("success", False)),
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def fetch_analyses(user_id: str, start_date: str) -> AgentResult:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "get_patient_analyses",
                {"data": {"user_id": user_id, "start_date": start_date}},
            )
        raw_results = response.structured_content or {}
        analyses_collection = raw_results.get("result", [])
        return {
            "success": True,
            "data": [AnalysisRecordSchema(**analysis) for analysis in analyses_collection],
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": [], "error": str(exc)}


async def update_analysis(analysis_id: str, data: UpdateAnalysisSchema) -> AgentResult:
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
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        if not analysis_data.get("success"):
            return {"success": False, "data": None, "error": analysis_data.get("error", f"Analysis {analysis_id} not found")}
        return {"success": True, "data": MutateAnalysisResponseSchema(success=True), "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def delete_analysis(analysis_id: str) -> AgentResult:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "delete_analysis",
                {"data": {"analysis_id": analysis_id}},
            )
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        if not analysis_data.get("success"):
            return {"success": False, "data": None, "error": analysis_data.get("error", f"Analysis {analysis_id} not found")}
        return {"success": True, "data": MutateAnalysisResponseSchema(success=True), "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def create_analyses_from_prompt(data: AnalysisByPromptRequestSchema) -> AgentResult:
    try:
        async with Client(settings.labs_agent_url) as client:
            response = await client.call_tool(
                "create_analyses_from_prompt",
                {"data": {"user_id": data.user_id, "prompt": data.prompt}},
            )
        raw_results = response.structured_content or {}
        analysis_data = raw_results.get("result", raw_results)
        return {
            "success": True,
            "data": AnalysisByPromptResponseSchema(
                success=analysis_data.get("success", False),
                list_missing_analysis=analysis_data.get("list_missing_analysis", []),
            ),
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}
