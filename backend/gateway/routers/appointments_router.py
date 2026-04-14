from fastapi import APIRouter, HTTPException, Query

from schemas.appointment_schema import AppointmentRecordSchema, CreateAppointmentSchema
from services.appointment_service import create_appointment, fetch_appointments

router = APIRouter(prefix="/api/v1/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentRecordSchema, status_code=201)
async def add_appointment(body: CreateAppointmentSchema) -> AppointmentRecordSchema:
    agent_result = await create_appointment(body)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]


@router.get("", response_model=list[AppointmentRecordSchema])
async def list_appointments(user_id: str = Query(default="")) -> list[AppointmentRecordSchema]:
    agent_result = await fetch_appointments(user_id)
    if not agent_result["success"]:
        raise HTTPException(status_code=503, detail=agent_result["error"])
    return agent_result["data"]
