SYSTEM_PROMPT = """Role: Synthetic Apple Watch/HealthKit generator (Series 9+).
Sleep (5–9.5h total): Deep (8–20%), Core (45–60%), REM (20–30%), Awake (0.1–0.8h). Efficiency: 78–96%.
Movement: Steps (2.5k–22k). Active kcal: Steps × 0.045–0.065. Resting kcal: 1.4k–2.2k. Exercise: 0–120m. Stand: 6–16h.
Vitals: HRV (SDNN: 15–110ms), Resting HR (44–80 BPM), Resp Rate (12–20 br/min).
Recovery: Score (30–98), VO2 Max (28–58), Body Battery (20–100%).
Logic: VO2 Max/Resting Energy are stable (±0.3/±30). HRV/Recovery inversely correlate with RHR. Exercise scales with Active kcal. Weekend variance applied. No physiological overflows.
"""


def user_prompt(user_id: str, dates: list[str]) -> str:
    return (
        f"Generate synthetic Apple HealthKit daily metrics for user '{user_id}' "
        f"for the following dates: {dates}.\n"
        "Return a JSON object with a single key 'records' containing an array of daily entries. "
        "Each entry must match the DailyHealthMetrics schema exactly."
    )
