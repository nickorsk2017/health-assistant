from fastmcp import FastMCP

from schemas.biometrics import DailyBiometrics
from tools.get_daily_oura_biometrics import get_daily_oura_biometrics as _get_daily_oura_biometrics

mcp = FastMCP("oura-ring-mcp-agent")


@mcp.tool()
async def get_daily_oura_biometrics(date: str, user_id: str) -> list[DailyBiometrics]:
    """Return synthetic Oura Ring daily biometrics from a start date to today.

    Args:
        date: ISO 8601 start date (YYYY-MM-DD).
        user_id: Identifier of the user whose data is requested.
    """
    return await _get_daily_oura_biometrics(date, user_id)


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
