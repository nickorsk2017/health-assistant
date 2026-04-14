from fastapi import APIRouter, HTTPException

from schemas.device_schema import (
    AddDeviceRequestSchema,
    AddDeviceResponseSchema,
    DeviceRecordSchema,
    RemoveDeviceResponseSchema,
)
from services.device_service import delete_device, fetch_patient_devices, register_device
from services.exceptions import AgentConnectionError, NoDataFoundError

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


@router.post("", response_model=AddDeviceResponseSchema, status_code=201)
async def create_device(body: AddDeviceRequestSchema) -> AddDeviceResponseSchema:
    try:
        return await register_device(body)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.delete("/{device_id}", response_model=RemoveDeviceResponseSchema)
async def remove_device(device_id: str) -> RemoveDeviceResponseSchema:
    try:
        return await delete_device(device_id)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except NoDataFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/{user_id}", response_model=list[DeviceRecordSchema])
async def list_patient_devices(user_id: str) -> list[DeviceRecordSchema]:
    try:
        return await fetch_patient_devices(user_id)
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
