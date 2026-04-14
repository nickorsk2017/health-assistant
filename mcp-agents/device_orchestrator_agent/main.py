import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP
from loguru import logger

from config import settings
from db.init import create_tables
from scheduler.poller import start_poller
from schemas.device import (
    AddDeviceRequest,
    AddDeviceResponse,
    DeviceWithLastSync,
    RemoveDeviceRequest,
    RemoveDeviceResponse,
)
from tools.add_device import add_device as _add_device
from tools.get_patient_devices import get_patient_devices as _get_patient_devices
from tools.remove_device import remove_device as _remove_device

logger.add("mcp.log", rotation="10 MB")

_poller_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    global _poller_task
    logger.info("Initialising database tables...")
    await create_tables()
    logger.info("Starting background poller...")
    _poller_task = asyncio.create_task(start_poller())
    try:
        yield
    finally:
        if _poller_task and not _poller_task.done():
            _poller_task.cancel()
            try:
                await _poller_task
            except asyncio.CancelledError:
                pass
        logger.info("Poller stopped.")


mcp = FastMCP("device-orchestrator-agent", lifespan=lifespan)


@mcp.resource("config://settings")
def get_config() -> str:
    return (
        f"poll_interval_seconds: {settings.poll_interval_seconds}\n"
        f"oura_ring_agent_url: {settings.oura_ring_agent_url}\n"
        f"apple_health_agent_url: {settings.apple_health_agent_url}"
    )


@mcp.tool(name="add_device")
async def add_device(data: AddDeviceRequest) -> dict:
    """Register a new wearable device for a patient and immediately fetch today's data.

    Args:
        user_id: UUID of the patient who owns the device.
        type_device: Device type — 'oura_ring' or 'apple_health'.
        diagnosis_mock: Optional diagnosis name used to generate condition-specific
            synthetic data (e.g. 'Pheochromocytoma'). Omit for healthy baseline.
    """
    result = await _add_device(data)
    return result.model_dump()


@mcp.tool(name="remove_device")
async def remove_device(data: RemoveDeviceRequest) -> dict:
    """Remove a device and all its associated logs.

    Args:
        device_id: UUID of the device to remove.
    """
    result = await _remove_device(data)
    return result.model_dump()


@mcp.tool(name="get_patient_devices")
async def get_patient_devices(user_id: str) -> list[dict]:
    """List all registered devices for a patient, including their latest sync timestamp.

    Args:
        user_id: UUID of the patient.
    """
    devices = await _get_patient_devices(user_id)
    return [d.model_dump() for d in devices]


def run() -> None:
    mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)

def run_inspector() -> None:
    mcp.run()
