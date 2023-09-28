"""Airzone Cloud API Zone device."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aioairzone_cloud.common import OperationMode

from .const import (
    API_CONFIG,
    API_META,
    API_MODE,
    API_MODE_AVAIL,
    API_NAME,
    API_POWER,
    API_SETPOINT,
    API_SYSTEM_NUMBER,
    API_VALUE,
    API_ZONE_NUMBER,
    AZD_MASTER,
    AZD_SYSTEM,
    AZD_SYSTEM_ID,
    AZD_ZONE,
)
from .hvac import HVAC

if TYPE_CHECKING:
    from .system import System


class Zone(HVAC):
    """Airzone Cloud Zone device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Zone device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.master: bool | None = None
        self.system: System | None = None

        if API_CONFIG in device_data:
            sub_data = device_data[API_CONFIG]
        else:
            sub_data = device_data[API_META]

        self.system_number = int(sub_data[API_SYSTEM_NUMBER])
        self.zone_number = int(sub_data[API_ZONE_NUMBER])

        if API_NAME in device_data:
            self.name = str(device_data[API_NAME])
        else:
            self.name = f"Zone {self.system_number}:{self.zone_number}"

    def data(self) -> dict[str, Any]:
        """Return Zone data."""
        data = super().data()

        data[AZD_MASTER] = self.get_master()
        data[AZD_SYSTEM] = self.get_system_num()
        data[AZD_ZONE] = self.get_zone()

        system_id = self.get_system_id()
        if system_id is not None:
            data[AZD_SYSTEM_ID] = system_id

        return data

    def get_master(self) -> bool:
        """Return Zone device master/slave."""
        return self.master or False

    def get_system_id(self) -> str | None:
        """Return Zone device System ID."""
        if self.system is not None:
            return self.system.get_id()
        return None

    def get_system_num(self) -> int:
        """Return System number."""
        return self.system_number

    def get_zone(self) -> int:
        """Return Zone number."""
        return self.zone_number

    def set_modes(self, modes: list[OperationMode]) -> None:
        """Set slave zone modes."""
        self.modes = modes

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update device parameter from API request."""

        if param == API_MODE:
            if self.system is not None:
                self.system.set_param(param, data)
            else:
                self.set_mode(data[API_VALUE])
        elif param == API_POWER:
            self.set_power(data[API_VALUE])
        elif param == API_SETPOINT:
            self.set_setpoint(data[API_VALUE])

    def set_system(self, system: System) -> None:
        """Set System."""
        self.system = system

    def update(self, data: dict[str, Any]) -> None:
        """Update Zone data."""
        super().update(data)

        if API_MODE_AVAIL in data:
            self.master = len(data[API_MODE_AVAIL]) > 0
        else:
            self.master = None
