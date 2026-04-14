from fastmcp import Client

from config import settings
from schemas.device_schema import (
    AddDeviceRequestSchema,
    AddDeviceResponseSchema,
    DeviceRecordSchema,
    RemoveDeviceResponseSchema,
)
from services.exceptions import AgentConnectionError, NoDataFoundError


async def register_device(data: AddDeviceRequestSchema) -> AddDeviceResponseSchema:
    try:
        async with Client(settings.device_orchestrator_agent_url) as client:
            result = await client.call_tool(
                "add_device",
                {
                    "data": {
                        "user_id": str(data.user_id),
                        "type_device": data.type_device,
                        "diagnosis_mock": data.diagnosis_mock,
                    }
                },
            )
    except Exception as exc:
        raise AgentConnectionError(f"device_orchestrator_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    if not payload.get("success"):
        raise AgentConnectionError("device_orchestrator_agent returned failure on add_device")

    return AddDeviceResponseSchema(
        success=True,
        device_id=payload.get("device_id", ""),
    )


async def delete_device(device_id: str) -> RemoveDeviceResponseSchema:
    try:
        async with Client(settings.device_orchestrator_agent_url) as client:
            result = await client.call_tool(
                "remove_device",
                {"data": {"device_id": device_id}},
            )
    except Exception as exc:
        raise AgentConnectionError(f"device_orchestrator_agent unreachable: {exc}") from exc

    payload = result.structured_content or {}
    if not payload.get("success"):
        raise NoDataFoundError(payload.get("error", f"Device {device_id} not found"))

    return RemoveDeviceResponseSchema(success=True)


async def fetch_patient_devices(user_id: str) -> list[DeviceRecordSchema]:
    try:
        async with Client(settings.device_orchestrator_agent_url) as client:
            result = await client.call_tool(
                "get_patient_devices",
                {"user_id": user_id},
            )
    except Exception as exc:
        raise AgentConnectionError(f"device_orchestrator_agent unreachable: {exc}") from exc

    payload = result.structured_content
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = payload.get("result", [])
    else:
        records = []

    return [DeviceRecordSchema(**r) for r in records]
