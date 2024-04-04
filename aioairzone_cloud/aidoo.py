"""Airzone Cloud API Aidoo device."""

from __future__ import annotations

from typing import Any

from .common import SpeedType, parse_int, parse_str
from .const import (
    API_MODE,
    API_NAME,
    API_POWER,
    API_SETPOINT,
    API_SP_AIR_COOL,
    API_SP_AIR_HEAT,
    API_SPEED_CONF,
    API_SPEED_TYPE,
    API_SPEED_VALUES,
    API_VALUE,
    AZD_SPEED,
    AZD_SPEED_TYPE,
    AZD_SPEEDS,
)
from .entity import EntityUpdate
from .hvac import HVAC


class Aidoo(HVAC):
    """Airzone Cloud Aidoo device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Aidoo device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.speed: int | None = None
        self.speeds: dict[int, int] = {}
        self.speed_type: SpeedType | None = None

        device_name = parse_str(device_data.get(API_NAME))
        if device_name is not None:
            self.name = device_name
        else:
            self.name = f"Aidoo {ws_id}"

    def data(self) -> dict[str, Any]:
        """Return Aidoo device data."""
        data = super().data()

        speed = self.get_speed()
        if speed is not None:
            data[AZD_SPEED] = speed

        speeds = self.get_speeds()
        if speeds is not None:
            data[AZD_SPEEDS] = speeds

        speed_type = self.get_speed_type()
        if speed_type is not None:
            data[AZD_SPEED_TYPE] = speed_type

        return data

    def get_speed(self) -> int | None:
        """Return Aidoo speed."""
        return self.speed

    def get_speeds(self) -> dict[int, int] | None:
        """Return Aidoo speeds."""
        if len(self.speeds) > 0:
            return self.speeds
        return None

    def get_speed_type(self) -> SpeedType | None:
        """Return Aidoo speed type."""
        return self.speed_type

    def set_speed(self, speed: int) -> None:
        """Set Aidoo speed."""
        if self.speed is not None:
            self.speed = speed

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

    def update_data(self, update: EntityUpdate) -> None:
        """Update Aidoo data."""
        super().update_data(update)

        data = update.get_data()

        speed = parse_int(data.get(API_SPEED_CONF))
        if speed is not None:
            self.speed = speed

        speed_type = data.get(API_SPEED_TYPE)
        if speed_type is not None:
            self.speed_type = SpeedType(speed_type)

        speeds_values: list[int] | None = data.get(API_SPEED_VALUES)
        if speeds_values is not None:
            speeds: dict[int, int] = {}

            if 0 in speeds_values:
                speeds[0] = 0

            speed_count = 1
            speeds_values.sort()
            for speed_value in speeds_values:
                if speed_value > 0:
                    speeds[speed_count] = int(speed_value)
                    speed_count += 1

            self.speeds = speeds
