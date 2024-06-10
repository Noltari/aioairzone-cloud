"""Airzone Cloud API Aidoo device."""

from __future__ import annotations

from typing import Any

from .common import parse_str
from .const import (
    API_MODE,
    API_NAME,
    API_POWER,
    API_SETPOINT,
    API_SP_AIR_COOL,
    API_SP_AIR_HEAT,
    API_SPEED_CONF,
    API_VALUE,
)
from .hvac import HVAC


class Aidoo(HVAC):
    """Airzone Cloud Aidoo device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Aidoo device init."""
        super().__init__(inst_id, ws_id, device_data)

        device_name = parse_str(device_data.get(API_NAME))
        if device_name is not None:
            self.name = device_name
        else:
            self.name = f"Aidoo {ws_id}"

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update device parameter from API request."""
        if param == API_MODE:
            self.set_mode(data[API_VALUE])
        elif param == API_POWER:
            self.set_power(data[API_VALUE])
        elif param == API_SETPOINT:
            self.set_setpoint(data[API_VALUE])
        elif param == API_SP_AIR_COOL:
            self.set_setpoint_cool(data[API_VALUE])
        elif param == API_SP_AIR_HEAT:
            self.set_setpoint_heat(data[API_VALUE])
        elif param == API_SPEED_CONF:
            self.set_speed(data[API_VALUE])
