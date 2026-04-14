from typing import Any, TypedDict


class AgentResult(TypedDict):
    success: bool
    data: Any  # Pydantic schema instance, list of instances, or None on failure
    error: str | None
