"""Airzone Cloud API Device."""
from __future__ import annotations

from typing import Any

from .common import OperationMode
from .const import (
    API_DEVICE_ID,
    API_IS_CONNECTED,
    API_MODE,
    API_MODE_AVAIL,
    AZD_CONNECTED,
    AZD_ID,
    AZD_INSTALLATION,
    AZD_MODE,
    AZD_MODES,
    AZD_NAME,
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
        self.mode: OperationMode | None = None
        self.modes: list[OperationMode] = []
        self.webserver_id = ws_id

        if API_IS_CONNECTED in device_data:
            self.connected = bool(device_data[API_IS_CONNECTED])

    def data(self) -> dict[str, Any]:
        """Return Device data."""
        data = {
            AZD_CONNECTED: self.get_connected(),
            AZD_ID: self.get_id(),
            AZD_INSTALLATION: self.get_installation(),
            AZD_MODE: self.get_mode(),
            AZD_NAME: self.get_name(),
            AZD_WEBSERVER: self.get_webserver(),
        }

        modes = self.get_modes()
        if modes:
            data[AZD_MODES] = modes

        return data

    def get_connected(self) -> bool:
        """Return connected status."""
        return self.connected

    def get_id(self) -> str:
        """Return Device ID."""
        return self.id

    def get_installation(self) -> str:
        """Return Installation ID."""
        return self.installation_id

    def get_mode(self) -> OperationMode | None:
        """Return Device mode."""
        return self.mode

    def get_modes(self) -> list[OperationMode] | None:
        """Return Device modes."""
        if len(self.modes) > 0:
            return self.modes
        return None

    def get_name(self) -> str:
        """Return Device name."""
        return self.name

    def get_webserver(self) -> str:
        """Return WebServer ID."""
        return self.webserver_id

    def update(self, data: dict[str, Any]) -> None:
        """Update Device data."""
        if API_IS_CONNECTED in data:
            self.connected = bool(data[API_IS_CONNECTED])

        if API_MODE in data:
            self.mode = OperationMode(data[API_MODE])
        if API_MODE_AVAIL in data and len(data[API_MODE_AVAIL]) > 0:
            modes = []
            for mode in data[API_MODE_AVAIL]:
                modes += [OperationMode(mode)]
            self.modes = modes
