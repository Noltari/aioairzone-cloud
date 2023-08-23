"""Airzone Cloud API Device."""
from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from typing import Any

from .common import OperationMode
from .const import (
    API_DEVICE_ID,
    API_ERRORS,
    API_IS_CONNECTED,
    API_MODE,
    API_MODE_AVAIL,
    API_WARNINGS,
    API_WS_CONNECTED,
    AZD_AVAILABLE,
    AZD_ERRORS,
    AZD_ID,
    AZD_INSTALLATION,
    AZD_IS_CONNECTED,
    AZD_MODE,
    AZD_MODE_AUTO,
    AZD_MODES,
    AZD_NAME,
    AZD_PROBLEMS,
    AZD_WARNINGS,
    AZD_WEBSERVER,
    AZD_WS_CONNECTED,
)

_LOGGER = logging.getLogger(__name__)


class Device(ABC):
    """Airzone Cloud Device."""

    name: str

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Device init."""
        self.auto_mode: OperationMode | None = None
        self.errors: list[str] = []
        self.id = str(device_data[API_DEVICE_ID])
        self.installation_id = inst_id
        self.mode: OperationMode | None = None
        self.modes: list[OperationMode] = []
        self.name: str = "Device"
        self.warnings: list[str] = []
        self.webserver_id = ws_id
        self.ws_connected: bool = True

        if API_IS_CONNECTED in device_data:
            self.is_connected = bool(device_data[API_IS_CONNECTED])
        else:
            self.is_connected = True

    def data(self) -> dict[str, Any]:
        """Return Device data."""
        data: dict[str, Any] = {
            AZD_AVAILABLE: self.get_available(),
            AZD_ID: self.get_id(),
            AZD_INSTALLATION: self.get_installation(),
            AZD_IS_CONNECTED: self.get_is_connected(),
            AZD_MODE: self.get_mode(),
            AZD_NAME: self.get_name(),
            AZD_PROBLEMS: self.get_problems(),
            AZD_WEBSERVER: self.get_webserver(),
            AZD_WS_CONNECTED: self.get_ws_connected(),
        }

        errors = self.get_errors()
        if len(errors) > 0:
            data[AZD_ERRORS] = errors

        mode_auto = self.get_mode_auto()
        if mode_auto is not None:
            data[AZD_MODE_AUTO] = mode_auto

        modes = self.get_modes()
        if modes is not None:
            data[AZD_MODES] = modes

        warnings = self.get_warnings()
        if len(warnings) > 0:
            data[AZD_WARNINGS] = warnings

        return data

    def get_available(self) -> bool:
        """Return availability status."""
        return self.is_connected and self.ws_connected

    def get_errors(self) -> list[str]:
        """Return Device errors."""
        return self.errors

    def get_id(self) -> str:
        """Return Device ID."""
        return self.id

    def get_installation(self) -> str:
        """Return Installation ID."""
        return self.installation_id

    def get_is_connected(self) -> bool:
        """Return Device connection status."""
        return self.is_connected

    def get_mode(self) -> OperationMode | None:
        """Return Device mode."""
        return self.mode

    def get_mode_auto(self) -> OperationMode | None:
        """Return current auto mode."""
        return self.auto_mode

    def get_modes(self) -> list[OperationMode] | None:
        """Return Device modes."""
        if len(self.modes) > 0:
            return self.modes
        return None

    def get_name(self) -> str:
        """Return Device name."""
        return self.name

    def get_problems(self) -> bool:
        """Return Device problems."""
        return bool(self.errors) or bool(self.warnings)

    def get_warnings(self) -> list[str]:
        """Return Device warnings."""
        return self.warnings

    def get_webserver(self) -> str:
        """Return WebServer ID."""
        return self.webserver_id

    def get_ws_connected(self) -> bool:
        """Return WebServer connection status."""
        return self.ws_connected

    def set_mode(self, mode: int | OperationMode) -> None:
        """Set device operation mode."""
        _mode = OperationMode(mode)
        if _mode in self.modes:
            self.mode = _mode
        else:
            _LOGGER.error("%s: mode %s not in %s", self.id, _mode, self.modes)

    @abstractmethod
    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update device parameter from API request."""

    def update(self, data: dict[str, Any]) -> None:
        """Update Device data."""
        is_connected = data.get(API_IS_CONNECTED)
        if is_connected is not None:
            self.is_connected = bool(is_connected)
        ws_connected = data.get(API_WS_CONNECTED)
        if ws_connected is not None:
            self.ws_connected = bool(ws_connected)

        errors = data.get(API_ERRORS)
        if errors is not None:
            self.errors = []
            for error in errors:
                self.errors += [error]

        mode = data.get(API_MODE)
        if mode is not None:
            self.mode = OperationMode(mode)
        mode_avail = data.get(API_MODE_AVAIL)
        if mode_avail is not None and len(mode_avail) > 0:
            modes = []
            for mode in mode_avail:
                modes += [OperationMode(mode)]
            self.modes = modes

        warnings = data.get(API_WARNINGS)
        if warnings is not None:
            self.warnings = []
            for warning in warnings:
                self.warnings += [warning]
