"""Airzone Cloud API System."""
from __future__ import annotations

from typing import Any

from .const import API_CONFIG, API_META, API_SYSTEM_NUMBER, AZD_SYSTEM
from .device import Device


class System(Device):
    """Airzone Cloud System device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud System device init."""
        super().__init__(inst_id, ws_id, device_data)

        if API_CONFIG in device_data:
            sub_data = device_data[API_CONFIG]
        else:
            sub_data = device_data[API_META]

        self.system_number = int(sub_data[API_SYSTEM_NUMBER])

        self.name = f"System {self.system_number}"

    def data(self) -> dict[str, Any]:
        """Return System device data."""
        data = super().data()

        data[AZD_SYSTEM] = self.get_system()

        return data

    def get_system(self) -> int:
        """Return System number."""
        return self.system_number
