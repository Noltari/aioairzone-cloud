"""Airzone Cloud API Output."""

from __future__ import annotations

import logging
from typing import Any

from .const import API_SYSTEM_NUMBER, AZD_SYSTEM
from .device import Device
from .entity import EntityUpdate

_LOGGER = logging.getLogger(__name__)


class Output(Device):
    """Airzone Cloud Output device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Output device init."""
        super().__init__(inst_id, ws_id, device_data)

        sub_data = self.sub_data(device_data)
        self.system_number = int(sub_data[API_SYSTEM_NUMBER])

        self.name = f"Output {self.system_number}"

    def data(self) -> dict[str, Any]:
        """Return System device data."""
        data = super().data()

        data[AZD_SYSTEM] = self.get_system_num()

        return data

    def get_system_num(self) -> int:
        """Return System number."""
        return self.system_number

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update Output parameter from API request."""

    def update_data(self, update: EntityUpdate) -> None:
        """Update Output data."""
        super().update_data(update)

        data = update.get_data()

        _LOGGER.debug("output: %s", data)
