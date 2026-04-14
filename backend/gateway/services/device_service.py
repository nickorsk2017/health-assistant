from fastmcp import Client

from config import settings
from schemas.device_schema import (
    AddDeviceRequestSchema,
    AddDeviceResponseSchema,
    DeviceRecordSchema,
    RemoveDeviceResponseSchema,
)
from services.agent_result import AgentResult


async def register_device(data: AddDeviceRequestSchema) -> AgentResult:
    try:
        async with Client(settings.device_orchestrator_agent_url) as client:
            response = await client.call_tool(
                "add_device",
                {
                    "data": {
                        "user_id": str(data.user_id),
                        "type_device": data.type_device,
                        "diagnosis_mock": data.diagnosis_mock,
                    }
                },
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": "device_orchestrator_agent returned failure on add_device"}
        return {
            "success": True,
            "data": AddDeviceResponseSchema(
                success=True,
                device_id=raw_results.get("device_id", ""),
            ),
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def delete_device(device_id: str) -> AgentResult:
    try:
        async with Client(settings.device_orchestrator_agent_url) as client:
            response = await client.call_tool(
                "remove_device",
                {"data": {"device_id": device_id}},
            )
        raw_results = response.structured_content or {}
        if not raw_results.get("success"):
            return {"success": False, "data": None, "error": raw_results.get("error", f"Device {device_id} not found")}
        return {"success": True, "data": RemoveDeviceResponseSchema(success=True), "error": None}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


async def fetch_patient_devices(user_id: str) -> AgentResult:
    try:
        async with Client(settings.device_orchestrator_agent_url) as client:
            response = await client.call_tool(
                "get_patient_devices",
                {"user_id": user_id},
            )
        raw_results = response.structured_content
        devices_collection = (
            raw_results if isinstance(raw_results, list)
            else raw_results.get("result", []) if isinstance(raw_results, dict)
            else []
        )
        return {
            "success": True,
            "data": [DeviceRecordSchema(**device) for device in devices_collection],
            "error": None,
        }
    except Exception as exc:
        return {"success": False, "data": [], "error": str(exc)}
