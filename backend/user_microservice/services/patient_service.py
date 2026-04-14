from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Patient
from schemas.patient_schema import CreatePatientSchema


async def upsert_patient(session: AsyncSession, data: CreatePatientSchema) -> Patient:
    if data.email:
        result = await session.execute(select(Patient).where(Patient.email == data.email))
        existing = result.scalar_one_or_none()
        if existing:
            existing.full_name = data.full_name
            existing.dob = data.dob
            existing.gender = data.gender
            await session.commit()
            await session.refresh(existing)
            return existing

    patient = Patient(
        full_name=data.full_name,
        dob=data.dob,
        gender=data.gender,
        email=data.email,
    )
    session.add(patient)
    await session.commit()
    await session.refresh(patient)
    return patient


async def list_patients(session: AsyncSession) -> list[Patient]:
    result = await session.execute(select(Patient).order_by(Patient.created_at))
    return list(result.scalars().all())
