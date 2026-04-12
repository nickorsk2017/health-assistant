from pydantic import BaseModel

from schemas.health_metrics import DailyHealthMetrics


class GetAppleHealthMetricsRequest(BaseModel):
    date: str
    user_id: str


class GetAppleHealthMetricsResponse(BaseModel):
    records: list[DailyHealthMetrics]
