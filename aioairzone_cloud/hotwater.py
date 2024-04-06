"""Airzone Cloud API Domestic Hot Water."""

from __future__ import annotations

from typing import Any

from .common import HotWaterOperation, parse_bool, parse_float, parse_int
from .const import (
    API_ACTIVE,
    API_CELSIUS,
    API_DEFAULT_TEMP_STEP_ACS,
    API_POWER,
    API_POWERFUL_MODE,
    API_RANGE_SP_MAX_ACS,
    API_RANGE_SP_MIN_ACS,
    API_SETPOINT,
    API_STEP,
    API_TANK_TEMP,
    API_VALUE,
    AZD_ACTIVE,
    AZD_OPERATION,
    AZD_OPERATIONS,
    AZD_POWER,
    AZD_POWER_MODE,
    AZD_TEMP,
    AZD_TEMP_SET,
    AZD_TEMP_SET_MAX,
    AZD_TEMP_SET_MIN,
    AZD_TEMP_STEP,
)
from .device import Device
from .entity import EntityUpdate, UpdateType


class HotWater(Device):
    """Airzone Cloud Domestic Hot Water device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud DHW device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.active: bool | None = None
        self.name: str = "Airzone Cloud DHW"
        self.power: bool | None = None
        self.power_mode: bool | None = None
        self.temp_set_max: int | None = None
        self.temp_set_min: int | None = None
        self.temp_set: int | None = None
        self.temp: float | None = None
        self.temp_step: int | None = None

    def data(self) -> dict[str, Any]:
        """Return DHW device data."""
        data = super().data()

        data[AZD_ACTIVE] = self.get_active()
        data[AZD_OPERATION] = self.get_operation()
        data[AZD_OPERATIONS] = self.get_operations()
        data[AZD_POWER] = self.get_power()
        data[AZD_TEMP] = self.get_temperature()
        data[AZD_TEMP_SET] = self.get_temp_set()
        data[AZD_TEMP_SET_MAX] = self.get_temp_set_max()
        data[AZD_TEMP_SET_MIN] = self.get_temp_set_min()
        data[AZD_TEMP_STEP] = self.get_temp_step()

        power_mode = self.get_power_mode()
        if power_mode is not None:
            data[AZD_POWER_MODE] = power_mode

        return data

    def get_active(self) -> bool | None:
        """Return DHW device active status."""
        return self.active

    def get_operation(self) -> HotWaterOperation:
        """Return DHW current operation."""
        if self.get_power():
            if self.get_power_mode():
                return HotWaterOperation.Powerful
            return HotWaterOperation.On
        return HotWaterOperation.Off

    def get_operations(self) -> list[HotWaterOperation]:
        """Return DHW operation list."""
        operations = [
            HotWaterOperation.Off,
            HotWaterOperation.On,
        ]
        if self.get_power_mode() is not None:
            operations += [HotWaterOperation.Powerful]
        return operations

    def get_power(self) -> bool | None:
        """Return DHW device power."""
        return self.power

    def get_power_mode(self) -> bool | None:
        """Return DHW device power_mode."""
        return self.power_mode

    def get_temperature(self) -> float | None:
        """Return DHW device temperature."""
        if self.temp is not None:
            return round(self.temp, 1)
        return None

    def get_temp_set(self) -> int | None:
        """Return DHW device temperature setpoint."""
        return self.temp_set

    def get_temp_set_max(self) -> int | None:
        """Return DHW device max setpoint."""
        return self.temp_set_max

    def get_temp_set_min(self) -> int | None:
        """Return DHW device min setpoint."""
        return self.temp_set_min

    def get_temp_step(self) -> int | None:
        """Return DHW device temperature step."""
        if self.temp_step is not None:
            return self.temp_step
        return API_DEFAULT_TEMP_STEP_ACS

    def set_power(self, power: bool) -> None:
        """Set DHW power."""
        self.power = power

    def set_powerful_mode(self, powerful_mode: bool) -> None:
        """Set DHW powerful mode."""
        self.power_mode = powerful_mode

    def set_setpoint(self, setpoint: int) -> None:
        """Set DHW setpoint."""
        if self.temp_set is not None:
            self.temp_set = setpoint

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update DHW parameter from API request."""
        if param == API_POWER:
            self.set_power(data[API_VALUE])
        elif param == API_POWERFUL_MODE:
            self.set_powerful_mode(data[API_VALUE])
        elif param == API_SETPOINT:
            self.set_setpoint(data[API_VALUE])

    def update_data(self, update: EntityUpdate) -> None:
        """Update DHW device data."""
        super().update_data(update)

        data = update.get_data()

        if API_ACTIVE in data:
            active = parse_bool(data.get(API_ACTIVE))
            if active is not None:
                self.active = active
            else:
                # API sends active as null instead of False
                self.active = False
        else:
            if update.get_type() != UpdateType.WS_PARTIAL:
                self.active = None

        power = parse_bool(data.get(API_POWER))
        if power is not None:
            self.power = power

        powerful_mode = parse_bool(data.get(API_POWERFUL_MODE))
        if powerful_mode is not None:
            self.power_mode = powerful_mode

        range_sp_max_acs = parse_int(
            data.get(API_RANGE_SP_MAX_ACS, {}).get(API_CELSIUS)
        )
        if range_sp_max_acs is not None:
            self.temp_set_max = range_sp_max_acs

        range_sp_min_acs = parse_int(
            data.get(API_RANGE_SP_MIN_ACS, {}).get(API_CELSIUS)
        )
        if range_sp_min_acs is not None:
            self.temp_set_min = range_sp_min_acs

        setpoint = parse_int(data.get(API_SETPOINT, {}).get(API_CELSIUS))
        if setpoint is not None:
            self.temp_set = setpoint

        step = parse_int(data.get(API_STEP, {}).get(API_CELSIUS))
        if step is not None:
            self.temp_step = step

        tank_temp = parse_float(data.get(API_TANK_TEMP, {}).get(API_CELSIUS))
        if tank_temp is not None:
            self.temp = tank_temp
