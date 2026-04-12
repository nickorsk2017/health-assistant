from pydantic import BaseModel

from schemas.biometrics import DailyBiometrics


class GetDailyBiometricsRequest(BaseModel):
    date: str
    user_id: str


class GetDailyBiometricsResponse(BaseModel):
    records: list[DailyBiometrics]
