from typing import TypedDict


class ConsiliumState(TypedDict):
    user_id: str
    start_date: str
    history_records: list[dict]
    lab_records: list[dict]
    history_error: str | None
    labs_error: str | None
    consilium_findings: list[dict]


class GPDiagnosisState(TypedDict):
    user_id: str
    start_date: str
    history_records: list[dict]
    lab_records: list[dict]
    device_records: list[dict]
    complaint_records: list[dict]
    history_error: str | None
    labs_error: str | None
    devices_error: str | None
    complaints_error: str | None
    consilium_findings: list[dict]
    consultation: dict
    validation_result: dict
