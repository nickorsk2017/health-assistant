from datetime import date, timedelta

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger

from config import settings
from prompts.health_metrics_generation import SYSTEM_PROMPT, user_prompt
from schemas.health_metrics import DailyHealthMetrics
from schemas.http import GetAppleHealthMetricsResponse


def _date_range(start: date, end: date) -> list[str]:
    total_days = (end - start).days + 1
    return [(start + timedelta(days=i)).isoformat() for i in range(total_days)]


async def get_apple_health_metrics(date_str: str, user_id: str) -> list[DailyHealthMetrics]:
    start_date = date.fromisoformat(date_str)
    today = date.today()

    if start_date > today:
        raise ValueError(f"start date {date_str} is in the future")

    dates = _date_range(start_date, today)
    logger.info(f"Generating Apple Health metrics for user={user_id}, dates={dates[0]}..{dates[-1]}")

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.9,
    )
    structured_llm = llm.with_structured_output(GetAppleHealthMetricsResponse)

    response: GetAppleHealthMetricsResponse = await structured_llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt(user_id, dates)),
    ])

    return response.records
