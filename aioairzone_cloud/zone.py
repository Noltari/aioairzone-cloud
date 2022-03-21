"""Airzone Cloud API Zone."""
from __future__ import annotations

from typing import Any

from .const import API_CONFIG, API_NAME, API_ZONE_NUMBER, AZD_ZONE
from .device import Device


class Zone(Device):
    """Airzone Cloud Zone."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Zone init."""
        super().__init__(inst_id, ws_id, device_data)

        self.name = str(device_data[API_NAME])
        self.zone_number = int(device_data[API_CONFIG][API_ZONE_NUMBER])

    def data(self) -> dict[str, Any]:
        """Return Zone data."""
        data = super().data()
        data[AZD_ZONE] = self.get_zone()
        return data

    def get_zone(self) -> int:
        """Return Zone number."""
        return self.zone_number
