import sys
import uuid
from datetime import date
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import insert

from config import settings
from db.engine import SessionLocal
from db.models import Visit
from schemas.http import CreateVisitsFromPromptRequest, CreateVisitsFromPromptResponse
from schemas.visit import DoctorType

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "visit_parser.md"
_FALLBACK_DOCTOR_TYPE = DoctorType.general_practitioner

logger.add(sys.stderr, level="INFO")


class _ParsedVisit(BaseModel):
    visit_at: str = Field(description="ISO 8601 date YYYY-MM-DD.")
    doctor_type: str = Field(description="Medical specialty value from the allowed list.")
    subjective: str = Field(description="Patient complaints and reported symptoms.")
    objective: str = Field(description="Clinical findings, vitals, examination results.")
    assessment: str = Field(description="Clinical impression or diagnosis.")
    plan: str = Field(description="Treatment plan, prescriptions, follow-up.")


class _ParsedVisitList(BaseModel):
    visits: list[_ParsedVisit] = Field(description="All extracted visits from the prompt.")


def _coerce_doctor_type(raw: str) -> DoctorType:
    try:
        return DoctorType(raw.lower().strip())
    except ValueError:
        logger.warning(f"Unknown doctor_type '{raw}', defaulting to general_practitioner")
        return _FALLBACK_DOCTOR_TYPE


def _coerce_date(raw: str) -> date:
    try:
        parsed = date.fromisoformat(raw)
        return min(parsed, date.today())
    except (ValueError, TypeError):
        logger.warning(f"Could not parse date '{raw}', using today")
        return date.today()


def _fill_missing(value: str) -> str:
    if not value or not value.strip():
        return "Data not provided"
    return value.strip()


async def create_visits_from_prompt(
    data: CreateVisitsFromPromptRequest,
) -> CreateVisitsFromPromptResponse:
    system_prompt = _PROMPT_PATH.read_text(encoding="utf-8").replace(
        "{{TODAY}}", date.today().isoformat()
    )

    logger.info(f"Parsing prompt for user={data.user_id}, chars={len(data.prompt)}")

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.0,
    )
    structured_llm = llm.with_structured_output(_ParsedVisitList)
    parsed: _ParsedVisitList = await structured_llm.ainvoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=data.prompt),
        ]
    )

    if not parsed.visits:
        logger.warning(f"LLM returned no visits for user={data.user_id}")
        return CreateVisitsFromPromptResponse(success=True, count=0)

    logger.info(f"LLM extracted {len(parsed.visits)} visit(s)")

    async with SessionLocal() as session:
        for visit in parsed.visits:
            await session.execute(
                insert(Visit).values(
                    id=uuid.uuid4(),
                    user_id=data.user_id,
                    doctor_type=_coerce_doctor_type(visit.doctor_type).value,
                    visit_at=_coerce_date(visit.visit_at),
                    subjective=_fill_missing(visit.subjective),
                    objective=_fill_missing(visit.objective),
                    assessment=_fill_missing(visit.assessment),
                    plan=_fill_missing(visit.plan),
                )
            )
        await session.commit()

    logger.info(f"Saved {len(parsed.visits)} visit(s) for user={data.user_id}")
    return CreateVisitsFromPromptResponse(success=True, count=len(parsed.visits))
