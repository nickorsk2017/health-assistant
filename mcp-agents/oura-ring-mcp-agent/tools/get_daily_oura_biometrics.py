from datetime import date, timedelta

from openai import AsyncOpenAI

from config import settings
from prompts.biometrics_generation import SYSTEM_PROMPT, user_prompt
from schemas.biometrics import DailyBiometrics
from schemas.http import GetDailyBiometricsResponse


def _date_range(start: date, end: date) -> list[str]:
    total_days = (end - start).days + 1
    return [(start + timedelta(days=i)).isoformat() for i in range(total_days)]


async def get_daily_oura_biometrics(date_str: str, user_id: str) -> list[DailyBiometrics]:
    start_date = date.fromisoformat(date_str)
    today = date.today()

    if start_date > today:
        raise ValueError(f"start date {date_str} is in the future")

    dates = _date_range(start_date, today)

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    completion = await client.beta.chat.completions.parse(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt(user_id, dates)},
        ],
        response_format=GetDailyBiometricsResponse,
        temperature=0.9,
    )

    response = completion.choices[0].message.parsed
    if response is None:
        raise RuntimeError("LLM returned an empty or unparseable response")

    return response.records
