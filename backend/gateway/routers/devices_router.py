from fastapi import APIRouter, HTTPException

from schemas.device_schema import (
    AddDeviceRequestSchema,
    AddDeviceResponseSchema,
    DeviceRecordSchema,
    RemoveDeviceResponseSchema,
)
from services.device_service import delete_device, fetch_patient_devices, register_device

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


@router.post("", response_model=AddDeviceResponseSchema, status_code=201)
async def create_device(body: AddDeviceRequestSchema) -> AddDeviceResponseSchema:
    agent_result = await register_device(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.delete("/{device_id}", response_model=RemoveDeviceResponseSchema)
async def remove_device(device_id: str) -> RemoveDeviceResponseSchema:
    agent_result = await delete_device(device_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.get("/{user_id}", response_model=list[DeviceRecordSchema])
async def list_patient_devices(user_id: str) -> list[DeviceRecordSchema]:
    agent_result = await fetch_patient_devices(user_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]
