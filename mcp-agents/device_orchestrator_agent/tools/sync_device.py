import json
import uuid
from datetime import date, datetime, timezone

from fastmcp import Client
from loguru import logger
from sqlalchemy import insert

from config import settings
from db.engine import SessionLocal
from db.models import Device, DeviceLog
from schemas.device import DeviceWithLastSync


async def _call_oura_agent(device: Device) -> list[dict]:
    today = date.today().isoformat()
    async with Client(settings.oura_ring_agent_url) as client:
        result = await client.call_tool(
            "get_daily_oura_biometrics",
            {
                "date": today,
                "user_id": device.user_id,
                "diagnosis_mock": device.diagnosis_mock or "",
            },
        )
    payload = result.structured_content
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return payload.get("result", [payload])
    return []


async def _call_apple_agent(device: Device) -> list[dict]:
    today = date.today().isoformat()
    async with Client(settings.apple_health_agent_url) as client:
        result = await client.call_tool(
            "get_apple_health_metrics",
            {
                "date": today,
                "user_id": device.user_id,
                "diagnosis_mock": device.diagnosis_mock or "",
            },
        )
    payload = result.structured_content
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return payload.get("result", [payload])
    return []


async def sync_device(device: Device) -> bool:
    """Fetch today's data from the device agent and persist it as a log entry.

    Returns True if sync succeeded, False otherwise.
    """
    try:
        if device.type_device == "oura_ring":
            records = await _call_oura_agent(device)
        elif device.type_device == "apple_health":
            records = await _call_apple_agent(device)
        else:
            logger.warning(f"Unknown device type '{device.type_device}' for device {device.id}")
            return False

        log_payload = {
            "device_id": str(device.id),
            "type_device": device.type_device,
            "user_id": device.user_id,
            "diagnosis_mock": device.diagnosis_mock,
            "sync_date": date.today().isoformat(),
            "records": records,
        }
        log_str = json.dumps(log_payload, default=str, indent=2)
        now = datetime.now(timezone.utc)

        async with SessionLocal() as session:
            await session.execute(
                insert(DeviceLog).values(
                    id=uuid.uuid4(),
                    device_id=device.id,
                    log=log_str,
                    date_log=now,
                )
            )
            await session.commit()

        logger.info(f"Synced device {device.id} ({device.type_device}), {len(records)} record(s)")
        return True

    except Exception as exc:
        logger.error(f"Sync failed for device {device.id}: {exc}")
        return False
