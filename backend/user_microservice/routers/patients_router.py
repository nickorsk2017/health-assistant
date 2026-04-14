from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import AsyncSessionFactory
from schemas.patient_schema import CreatePatientSchema, PatientSchema
from services import patient_service

router = APIRouter(prefix="/patients", tags=["patients"])


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session


@router.post("", response_model=PatientSchema, status_code=201)
async def create_patient(
    body: CreatePatientSchema,
    session: AsyncSession = Depends(get_session),
) -> PatientSchema:
    return await patient_service.upsert_patient(session, body)


@router.get("", response_model=list[PatientSchema])
async def list_patients(
    session: AsyncSession = Depends(get_session),
) -> list[PatientSchema]:
    return await patient_service.list_patients(session)
