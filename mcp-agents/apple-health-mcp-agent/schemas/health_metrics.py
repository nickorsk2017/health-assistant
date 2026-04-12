from pydantic import BaseModel, Field


class SleepCycles(BaseModel):
    total_hours: float = Field(description="Total time asleep in hours.")
    deep_hours: float = Field(description="Deep (N3) sleep duration in hours.")
    core_hours: float = Field(description="Core (N1+N2) sleep duration in hours.")
    rem_hours: float = Field(description="REM sleep duration in hours.")
    awake_hours: float = Field(description="Time awake after sleep onset in hours.")
    sleep_efficiency_percent: float = Field(description="Sleep efficiency as a percentage.")
    time_in_bed_hours: float = Field(description="Total time in bed in hours.")


class MovementMetrics(BaseModel):
    steps: int = Field(description="Total step count for the day.")
    active_energy_kcal: float = Field(description="Active calories burned in kcal.")
    resting_energy_kcal: float = Field(description="Resting (basal) calories burned in kcal.")
    exercise_minutes: int = Field(description="Minutes of elevated-heart-rate exercise.")
    stand_hours: int = Field(ge=0, le=24, description="Hours with at least one minute of standing.")
    distance_km: float = Field(description="Total walking and running distance in kilometres.")
    flights_climbed: int = Field(description="Number of flights of stairs climbed.")


class StressMetrics(BaseModel):
    hrv_sdnn_ms: float = Field(description="HRV measured as SDNN in milliseconds (Apple Watch metric).")
    resting_heart_rate_bpm: int = Field(description="Resting heart rate in BPM.")
    walking_heart_rate_avg_bpm: int = Field(description="Average heart rate during walks in BPM.")
    respiratory_rate_rpm: float = Field(description="Breathing rate at rest in breaths per minute.")


class RecoveryMetrics(BaseModel):
    score: int = Field(ge=0, le=100, description="Derived recovery score (0-100) based on sleep and HRV.")
    cardio_fitness_vo2max: float = Field(description="Estimated VO2 max in mL/kg/min.")
    body_battery_percent: int = Field(ge=0, le=100, description="Estimated energy reserve as a percentage.")


class DailyHealthMetrics(BaseModel):
    date: str = Field(description="ISO 8601 date string (YYYY-MM-DD).")
    user_id: str = Field(description="Identifier of the user this record belongs to.")
    sleep: SleepCycles
    movement: MovementMetrics
    stress: StressMetrics
    recovery: RecoveryMetrics


