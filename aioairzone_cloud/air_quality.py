"""Airzone Cloud API Air Quality."""

from __future__ import annotations

import logging
from typing import Any

from .common import parse_str
from .const import API_NAME, API_SYSTEM_NUMBER, API_ZONE_NUMBER, AZD_SYSTEM, AZD_ZONE
from .device import Device
from .entity import EntityUpdate

_LOGGER = logging.getLogger(__name__)


class AirQuality(Device):
    """Airzone Cloud Air Quality device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Air Quality device init."""
        super().__init__(inst_id, ws_id, device_data)

        sub_data = self.sub_data(device_data)
        self.system_number = int(sub_data[API_SYSTEM_NUMBER])
        self.zone_number = int(sub_data[API_ZONE_NUMBER])

        device_name = parse_str(device_data.get(API_NAME))
        if device_name is not None:
            self.name = device_name
        else:
            self.name = f"Air Quality {self.system_number}:{self.zone_number}"

    def data(self) -> dict[str, Any]:
        """Return System device data."""
        data = super().data()

        data[AZD_SYSTEM] = self.get_system_num()
        data[AZD_ZONE] = self.get_zone_num()

        return data

    def get_system_num(self) -> int:
        """Return System number."""
        return self.system_number

    def get_zone_num(self) -> int:
        """Return Zone number."""
        return self.zone_number

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update Air Quality parameter from API request."""

    def update_data(self, update: EntityUpdate) -> None:
        """Update Air Quality data."""
        super().update_data(update)

        data = update.get_data()

        _LOGGER.warning("air_quality: %s", data)
