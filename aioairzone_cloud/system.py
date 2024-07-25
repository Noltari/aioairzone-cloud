"""Airzone Cloud API System."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .common import parse_str
from .const import (
    API_MODE,
    API_SYSTEM_FW,
    API_SYSTEM_NUMBER,
    API_SYSTEM_TYPE,
    API_VALUE,
    AZD_FIRMWARE,
    AZD_MODEL,
    AZD_SYSTEM,
)
from .device import Device
from .entity import EntityUpdate

if TYPE_CHECKING:
    from .zone import Zone


class System(Device):
    """Airzone Cloud System device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud System device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.system_fw: str | None = None
        self.system_type: str | None = None
        self.zones: dict[str, Zone] = {}

        sub_data = self.sub_data(device_data)
        self.system_number = int(sub_data[API_SYSTEM_NUMBER])

        self.name = f"System {self.system_number}"

    def data(self) -> dict[str, Any]:
        """Return System device data."""
        data = super().data()

        data[AZD_SYSTEM] = self.get_system_num()

        system_fw = self.get_system_fw()
        if system_fw is not None:
            data[AZD_FIRMWARE] = system_fw

        system_type = self.get_system_type()
        if system_type is not None:
            data[AZD_MODEL] = system_type

        return data

    def add_zone(self, zone: Zone) -> None:
        """Add System zone."""
        zone_id = zone.get_id()
        if zone_id not in self.zones:
            self.zones[zone_id] = zone

    def get_system_fw(self) -> str | None:
        """Return System firmware."""
        return self.system_fw

    def get_system_num(self) -> int:
        """Return System number."""
        return self.system_number

    def get_system_type(self) -> str | None:
        """Return System type."""
        return self.system_type

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update System parameter from API request."""

        if param == API_MODE:
            self.set_mode(data[API_VALUE])
            for zone in self.zones.values():
                zone.set_mode(data[API_VALUE])

    def update_data(self, update: EntityUpdate) -> None:
        """Update System data."""
        super().update_data(update)

        data = update.get_data()

        system_fw = parse_str(data.get(API_SYSTEM_FW))
        if system_fw is not None:
            self.system_fw = system_fw

        system_type = parse_str(data.get(API_SYSTEM_TYPE))
        if system_type is not None:
            self.system_type = system_type
