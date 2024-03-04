"""Airzone Cloud API Device."""

from __future__ import annotations

from abc import abstractmethod
import logging
from typing import Any

from .common import OperationMode
from .const import (
    API_AQ_PM_1,
    API_AQ_PM_2P5,
    API_AQ_PM_10,
    API_AQ_PRESENT,
    API_AQ_QUALITY,
    API_AQ_STATUS,
    API_CONFIG,
    API_DEVICE_ID,
    API_ERRORS,
    API_IS_CONNECTED,
    API_META,
    API_MODE,
    API_MODE_AVAIL,
    API_SYSTEM_NUMBER,
    API_WARNINGS,
    API_WS_CONNECTED,
    AZD_AQ_INDEX,
    AZD_AQ_PM_1,
    AZD_AQ_PM_2P5,
    AZD_AQ_PM_10,
    AZD_AQ_PRESENT,
    AZD_AQ_STATUS,
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
from .entity import Entity, EntityUpdate

_LOGGER = logging.getLogger(__name__)


class Device(Entity):
    """Airzone Cloud Device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Device init."""
        super().__init__()

        self.auto_mode: OperationMode | None = None
        self.aq_pm_1: int | None = None
        self.aq_pm_2p5: int | None = None
        self.aq_pm_10: int | None = None
        self.aq_present: bool | None = None
        self.aq_status: str | None = None
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

    def sub_data(self, device_data: dict[str, Any]) -> dict[str, Any]:
        """Get Device sub data."""
        if API_META in device_data:
            meta: dict[str, Any] = device_data.get(API_META, {})
            if API_SYSTEM_NUMBER in meta:
                return meta

        if API_CONFIG in device_data:
            config: dict[str, Any] = device_data.get(API_CONFIG, {})
            if API_SYSTEM_NUMBER in config:
                return config

        return device_data

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

        aq_index = self.get_aq_index()
        if aq_index is not None:
            data[AZD_AQ_INDEX] = aq_index

        aq_pm_1 = self.get_aq_pm_1()
        if aq_pm_1 is not None:
            data[AZD_AQ_PM_1] = aq_pm_1

        aq_pm_2p5 = self.get_aq_pm_2p5()
        if aq_pm_2p5 is not None:
            data[AZD_AQ_PM_2P5] = aq_pm_2p5

        aq_pm_10 = self.get_aq_pm_10()
        if aq_pm_10 is not None:
            data[AZD_AQ_PM_10] = aq_pm_10

        aq_present = self.get_aq_present()
        if aq_present is not None:
            data[AZD_AQ_PRESENT] = aq_present

        aq_status = self.get_aq_status()
        if aq_status is not None:
            data[AZD_AQ_STATUS] = aq_status

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

    def get_aq_index(self) -> int | None:
        """Return HVAC device Air Quality index."""
        if self.aq_status is not None:
            for key, value in API_AQ_STATUS.items():
                if self.aq_status == key:
                    return value
        return None

    def get_aq_pm_1(self) -> int | None:
        """Return HVAC device Air Quality PM 1."""
        return self.aq_pm_1

    def get_aq_pm_2p5(self) -> int | None:
        """Return HVAC device Air Quality PM 2.5."""
        return self.aq_pm_2p5

    def get_aq_pm_10(self) -> int | None:
        """Return HVAC device Air Quality PM 10."""
        return self.aq_pm_10

    def get_aq_present(self) -> bool | None:
        """Return HVAC device Air Quality present."""
        return self.aq_present

    def get_aq_status(self) -> str | None:
        """Return HVAC device Air Quality status."""
        return self.aq_status

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

    def update_data(self, update: EntityUpdate) -> None:
        """Update Device data."""
        data = update.get_data()

        is_connected = data.get(API_IS_CONNECTED)
        if is_connected is not None:
            self.is_connected = bool(is_connected)
        ws_connected = data.get(API_WS_CONNECTED)
        if ws_connected is not None:
            self.ws_connected = bool(ws_connected)

        aq_pm_1 = data.get(API_AQ_PM_1)
        if aq_pm_1 is not None:
            self.aq_pm_1 = int(aq_pm_1)

        aq_pm_2p5 = data.get(API_AQ_PM_2P5)
        if aq_pm_2p5 is not None:
            self.aq_pm_2p5 = int(aq_pm_2p5)

        aq_pm_10 = data.get(API_AQ_PM_10)
        if aq_pm_10 is not None:
            self.aq_pm_10 = int(aq_pm_10)

        aq_present = data.get(API_AQ_PRESENT)
        if aq_present is not None:
            self.aq_present = bool(aq_present)

        aq_status = data.get(API_AQ_QUALITY)
        if aq_status is not None:
            self.aq_status = str(aq_status)

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
