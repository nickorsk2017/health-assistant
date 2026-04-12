from pydantic import BaseModel, Field


class SleepMetrics(BaseModel):
    score: int = Field(ge=0, le=100, description="Overall sleep quality score (0-100).")
    total_sleep_hours: float = Field(description="Total sleep duration in hours.")
    rem_sleep_hours: float = Field(description="REM sleep duration in hours.")
    deep_sleep_hours: float = Field(description="Deep sleep duration in hours.")
    efficiency_percent: float = Field(description="Sleep efficiency as a percentage.")


class MovementMetrics(BaseModel):
    steps: int = Field(description="Total steps taken during the day.")
    distance_km: float = Field(description="Total distance covered in kilometres.")
    active_calories: int = Field(description="Active calories burned.")
    activity_score: int = Field(ge=0, le=100, description="Overall activity score (0-100).")


class RecoveryMetrics(BaseModel):
    score: int = Field(ge=0, le=100, description="Overall readiness/recovery score (0-100).")
    hrv_ms: float = Field(description="Heart-rate variability in milliseconds (RMSSD).")
    resting_heart_rate: int = Field(description="Resting heart rate in BPM.")
    body_temperature_deviation: float = Field(
        description="Deviation from baseline body temperature in °C."
    )
    stress_score: int = Field(ge=0, le=100, description="Stress level score (0-100, higher = more stressed).")


class DailyBiometrics(BaseModel):
    date: str = Field(description="ISO 8601 date string (YYYY-MM-DD).")
    user_id: str = Field(description="Identifier of the user this record belongs to.")
    sleep: SleepMetrics
    movement: MovementMetrics
    recovery: RecoveryMetrics
