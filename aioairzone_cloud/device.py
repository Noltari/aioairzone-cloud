"""Airzone Cloud API Device."""
from __future__ import annotations

from typing import Any

from .const import (
    API_CONFIG,
    API_DEVICE_ID,
    API_IS_CONNECTED,
    API_SYSTEM_NUMBER,
    AZD_CONNECTED,
    AZD_ID,
    AZD_INSTALLATION,
    AZD_NAME,
    AZD_SYSTEM,
    AZD_WEBSERVER,
)


class Device:
    """Airzone Cloud Device."""

    connected: bool
    name: str

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Device init."""
        self.id = str(device_data[API_DEVICE_ID])
        self.installation_id = inst_id
        self.system_number = int(device_data[API_CONFIG][API_SYSTEM_NUMBER])
        self.webserver_id = ws_id

        if API_IS_CONNECTED in device_data:
            self.connected = bool(device_data[API_IS_CONNECTED])

    def data(self) -> dict[str, Any]:
        """Return Device data."""
        return {
            AZD_CONNECTED: self.get_connected(),
            AZD_ID: self.get_id(),
            AZD_INSTALLATION: self.get_installation(),
            AZD_NAME: self.get_name(),
            AZD_SYSTEM: self.get_system(),
            AZD_WEBSERVER: self.get_webserver(),
        }

    def get_connected(self) -> bool:
        """Return connected status."""
        return self.connected

    def get_id(self) -> str:
        """Return Device ID."""
        return self.id

    def get_installation(self) -> str:
        """Return Installation ID."""
        return self.installation_id

    def get_name(self) -> str:
        """Return name."""
        return self.name

    def get_system(self) -> int:
        """Return System number."""
        return self.system_number

    def get_webserver(self) -> str:
        """Return WebServer ID."""
        return self.webserver_id

    def update(self, data: dict[str, Any]) -> None:
        """Update Device data."""
        if API_IS_CONNECTED in data:
            self.connected = bool(data[API_IS_CONNECTED])
