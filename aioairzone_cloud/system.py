"""Airzone Cloud API System."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .const import API_MODE, API_SYSTEM_NUMBER, API_VALUE, AZD_SYSTEM
from .device import Device

if TYPE_CHECKING:
    from .zone import Zone


class System(Device):
    """Airzone Cloud System device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud System device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.zones: dict[str, Zone] = {}

        sub_data = self.sub_data(device_data)
        self.system_number = int(sub_data[API_SYSTEM_NUMBER])

        self.name = f"System {self.system_number}"

    def data(self) -> dict[str, Any]:
        """Return System device data."""
        data = super().data()

        data[AZD_SYSTEM] = self.get_system_num()

        return data

    def add_zone(self, zone: Zone) -> None:
        """Add System zone."""
        zone_id = zone.get_id()
        if zone_id not in self.zones:
            self.zones[zone_id] = zone

    def get_system_num(self) -> int:
        """Return System number."""
        return self.system_number

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update System parameter from API request."""

        if param == API_MODE:
            self.set_mode(data[API_VALUE])
            for zone in self.zones.values():
                zone.set_mode(data[API_VALUE])
