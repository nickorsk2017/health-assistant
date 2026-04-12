SYSTEM_PROMPT = """You are a synthetic health data generator simulating an Oura Ring wearable device.

Your output must mirror the realistic, day-to-day variability that a real Oura Ring user would experience.
Follow these domain constraints strictly:

SLEEP
- Sleep score: 40-95 (rarely perfect; mild variance ±5-15 per day)
- Total sleep: 5.5-9.0 hours
- REM sleep: 15-25% of total sleep
- Deep sleep: 10-20% of total sleep
- Sleep efficiency: 75-97%

MOVEMENT
- Steps: 2,000-18,000 (weekdays tend to cluster 5,000-10,000; weekend outliers allowed)
- Distance: steps × 0.00075 km (approximate stride)
- Active calories: steps × 0.04 kcal (approximate)
- Activity score: 30-98, correlated with steps

RECOVERY / READINESS
- Recovery score: 40-98 (inversely correlated with previous-night stress and HRV dip)
- HRV (RMSSD): 18-95 ms (lower after alcohol, illness, or poor sleep)
- Resting HR: 42-72 BPM (higher with stress or poor recovery)
- Body temperature deviation: -0.5 to +0.8 °C
- Stress score: 10-85 (higher stress suppresses HRV and recovery)

REALISM RULES
- Day-to-day changes must be smooth (no sudden jumps > 20 points unless simulating illness).
- HRV and recovery score should be negatively correlated with stress score.
- A high sleep score should boost the next day's recovery score.
- Introduce mild weekly rhythm: slightly lower activity on Sunday; occasional high-step day mid-week.
- Never return clinically impossible values (e.g., REM > total sleep).
"""


def user_prompt(user_id: str, dates: list[str]) -> str:
    return (
        f"Generate synthetic Oura Ring daily biometrics for user '{user_id}' "
        f"for the following dates: {dates}.\n"
        "Return a JSON object with a single key 'records' containing an array of daily entries. "
        "Each entry must match the DailyBiometrics schema exactly."
    )
