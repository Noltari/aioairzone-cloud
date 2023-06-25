"""Airzone Cloud API HVAC device."""
from __future__ import annotations

from typing import Any

from .common import OperationAction, OperationMode
from .const import (
    API_ACTIVE,
    API_CELSIUS,
    API_DEFAULT_TEMP_STEP,
    API_HUMIDITY,
    API_LOCAL_TEMP,
    API_POWER,
    API_RANGE_SP_MAX_COOL_AIR,
    API_RANGE_SP_MAX_DRY_AIR,
    API_RANGE_SP_MAX_EMERHEAT_AIR,
    API_RANGE_SP_MAX_HOT_AIR,
    API_RANGE_SP_MAX_STOP_AIR,
    API_RANGE_SP_MAX_VENT_AIR,
    API_RANGE_SP_MIN_COOL_AIR,
    API_RANGE_SP_MIN_DRY_AIR,
    API_RANGE_SP_MIN_EMERHEAT_AIR,
    API_RANGE_SP_MIN_HOT_AIR,
    API_RANGE_SP_MIN_STOP_AIR,
    API_RANGE_SP_MIN_VENT_AIR,
    API_SP_AIR_COOL,
    API_SP_AIR_DRY,
    API_SP_AIR_HEAT,
    API_SP_AIR_STOP,
    API_SP_AIR_VENT,
    API_STEP,
    AZD_ACTION,
    AZD_ACTIVE,
    AZD_HUMIDITY,
    AZD_POWER,
    AZD_TEMP,
    AZD_TEMP_SET,
    AZD_TEMP_SET_COOL_AIR,
    AZD_TEMP_SET_DRY_AIR,
    AZD_TEMP_SET_HOT_AIR,
    AZD_TEMP_SET_MAX,
    AZD_TEMP_SET_MAX_COOL_AIR,
    AZD_TEMP_SET_MAX_DRY_AIR,
    AZD_TEMP_SET_MAX_EMERHEAT_AIR,
    AZD_TEMP_SET_MAX_HOT_AIR,
    AZD_TEMP_SET_MAX_STOP_AIR,
    AZD_TEMP_SET_MAX_VENT_AIR,
    AZD_TEMP_SET_MIN,
    AZD_TEMP_SET_MIN_COOL_AIR,
    AZD_TEMP_SET_MIN_DRY_AIR,
    AZD_TEMP_SET_MIN_EMERHEAT_AIR,
    AZD_TEMP_SET_MIN_HOT_AIR,
    AZD_TEMP_SET_MIN_STOP_AIR,
    AZD_TEMP_SET_MIN_VENT_AIR,
    AZD_TEMP_SET_STOP_AIR,
    AZD_TEMP_SET_VENT_AIR,
    AZD_TEMP_STEP,
)
from .device import Device


class HVAC(Device):
    """Airzone Cloud HVAC device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud HVAC device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.active: bool | None = None
        self.humidity: int | None = None
        self.name: str = "HVAC"
        self.power: bool | None = None
        self.temp_set_max_cool_air: float | None = None
        self.temp_set_max_dry_air: float | None = None
        self.temp_set_max_emerheat_air: float | None = None
        self.temp_set_max_hot_air: float | None = None
        self.temp_set_max_stop_air: float | None = None
        self.temp_set_max_vent_air: float | None = None
        self.temp_set_min_cool_air: float | None = None
        self.temp_set_min_dry_air: float | None = None
        self.temp_set_min_emerheat_air: float | None = None
        self.temp_set_min_hot_air: float | None = None
        self.temp_set_min_stop_air: float | None = None
        self.temp_set_min_vent_air: float | None = None
        self.temp_set_cool_air: float | None = None
        self.temp_set_dry_air: float | None = None
        self.temp_set_hot_air: float | None = None
        self.temp_set_stop_air: float | None = None
        self.temp_set_vent_air: float | None = None
        self.temp: float | None = None
        self.temp_step: float | None = None

    def data(self) -> dict[str, Any]:
        """Return HVAC device data."""
        data = super().data()

        data[AZD_ACTION] = self.get_action()
        data[AZD_ACTIVE] = self.get_active()
        data[AZD_POWER] = self.get_power()
        data[AZD_TEMP] = self.get_temperature()
        data[AZD_TEMP_STEP] = self.get_temp_step()

        humidity = self.get_humidity()
        if humidity is not None:
            data[AZD_HUMIDITY] = humidity

        temp_set_max = self.get_temp_set_max()
        if temp_set_max is not None:
            data[AZD_TEMP_SET_MAX] = temp_set_max
        temp_set_max_cool_air = self.get_temp_set_max_cool_air()
        if temp_set_max_cool_air is not None:
            data[AZD_TEMP_SET_MAX_COOL_AIR] = temp_set_max_cool_air
        temp_set_max_dry_air = self.get_temp_set_max_dry_air()
        if temp_set_max_dry_air is not None:
            data[AZD_TEMP_SET_MAX_DRY_AIR] = temp_set_max_dry_air
        temp_set_max_emerheat_air = self.get_temp_set_max_emerheat_air()
        if temp_set_max_emerheat_air is not None:
            data[AZD_TEMP_SET_MAX_EMERHEAT_AIR] = temp_set_max_emerheat_air
        temp_set_max_hot_air = self.get_temp_set_max_hot_air()
        if temp_set_max_hot_air is not None:
            data[AZD_TEMP_SET_MAX_HOT_AIR] = temp_set_max_hot_air
        temp_set_max_stop_air = self.get_temp_set_max_stop_air()
        if temp_set_max_stop_air is not None:
            data[AZD_TEMP_SET_MAX_STOP_AIR] = temp_set_max_stop_air
        temp_set_max_vent_air = self.get_temp_set_max_vent_air()
        if temp_set_max_vent_air is not None:
            data[AZD_TEMP_SET_MAX_VENT_AIR] = temp_set_max_vent_air

        temp_set_min = self.get_temp_set_min()
        if temp_set_min is not None:
            data[AZD_TEMP_SET_MIN] = temp_set_min
        temp_set_min_cool_air = self.get_temp_set_min_cool_air()
        if temp_set_min_cool_air is not None:
            data[AZD_TEMP_SET_MIN_COOL_AIR] = temp_set_min_cool_air
        temp_set_min_dry_air = self.get_temp_set_min_dry_air()
        if temp_set_min_dry_air is not None:
            data[AZD_TEMP_SET_MIN_DRY_AIR] = temp_set_min_dry_air
        temp_set_min_emerheat_air = self.get_temp_set_min_emerheat_air()
        if temp_set_min_emerheat_air is not None:
            data[AZD_TEMP_SET_MIN_EMERHEAT_AIR] = temp_set_min_emerheat_air
        temp_set_min_hot_air = self.get_temp_set_min_hot_air()
        if temp_set_min_hot_air is not None:
            data[AZD_TEMP_SET_MIN_HOT_AIR] = temp_set_min_hot_air
        temp_set_min_stop_air = self.get_temp_set_min_stop_air()
        if temp_set_min_stop_air is not None:
            data[AZD_TEMP_SET_MIN_STOP_AIR] = temp_set_min_stop_air
        temp_set_min_vent_air = self.get_temp_set_min_vent_air()
        if temp_set_min_vent_air is not None:
            data[AZD_TEMP_SET_MIN_VENT_AIR] = temp_set_min_vent_air

        temp_set = self.get_temp_set()
        if temp_set is not None:
            data[AZD_TEMP_SET] = temp_set
        temp_set_cool_air = self.get_temp_set_cool_air()
        if temp_set_cool_air is not None:
            data[AZD_TEMP_SET_COOL_AIR] = temp_set_cool_air
        temp_set_dry_air = self.get_temp_set_dry_air()
        if temp_set_dry_air is not None:
            data[AZD_TEMP_SET_DRY_AIR] = temp_set_dry_air
        temp_set_hot_air = self.get_temp_set_hot_air()
        if temp_set_hot_air is not None:
            data[AZD_TEMP_SET_HOT_AIR] = temp_set_hot_air
        temp_set_stop_air = self.get_temp_set_stop_air()
        if temp_set_stop_air is not None:
            data[AZD_TEMP_SET_STOP_AIR] = temp_set_stop_air
        temp_set_vent_air = self.get_temp_set_vent_air()
        if temp_set_vent_air is not None:
            data[AZD_TEMP_SET_VENT_AIR] = temp_set_vent_air

        return data

    def get_action(self) -> OperationAction:
        """Return HVAC action."""

        if self.get_power():
            if self.get_active():
                mode = self.get_mode() or OperationMode.STOP
                if mode.is_cool():
                    action = OperationAction.COOLING
                elif mode.is_heat():
                    action = OperationAction.HEATING
                elif mode.is_vent():
                    action = OperationAction.FAN
                elif mode.is_dry():
                    action = OperationAction.DRYING
                elif mode.is_auto():
                    action = self.get_auto_mode()
                else:
                    action = OperationAction.OFF
            else:
                action = OperationAction.IDLE
        else:
            action = OperationAction.OFF

        return action

    def get_active(self) -> bool | None:
        """Return HVAC device active status."""
        return self.active

    def get_auto_mode(self) -> OperationAction:
        """Return action from auto mode."""
        temp_sp = self.get_temp_set()
        temp_min = self.get_temp_set_min()
        temp_max = self.get_temp_set_max()
        cool_sp = self.get_temp_set_cool_air()
        cool_max = self.get_temp_set_max_cool_air()
        cool_min = self.get_temp_set_min_cool_air()
        heat_sp = self.get_temp_set_hot_air()
        heat_max = self.get_temp_set_max_hot_air()
        heat_min = self.get_temp_set_min_hot_air()

        if (
            cool_max is not None
            and cool_min is not None
            and heat_max is not None
            and heat_min is not None
        ):
            cool_match = cool_max == temp_max and cool_min == temp_min
            heat_match = heat_max == temp_max and heat_min == temp_min

            if cool_match and not heat_match:
                return OperationAction.COOLING
            if heat_match and not cool_match:
                return OperationAction.HEATING

        if cool_sp is not None and heat_sp is not None:
            cool_match = cool_sp == temp_sp
            heat_match = heat_sp == temp_sp

            if cool_match and not heat_match:
                return OperationAction.COOLING
            if heat_match and not cool_match:
                return OperationAction.HEATING

        return OperationAction.IDLE

    def get_humidity(self) -> int | None:
        """Return HVAC device humidity."""
        return self.humidity

    def get_power(self) -> bool | None:
        """Return HVAC device power."""
        return self.power

    def get_temperature(self) -> float | None:
        """Return HVAC device temperature."""
        if self.temp is not None:
            return round(self.temp, 1)
        return None

    def get_temp_set(self) -> float | None:
        """Return HVAC device temperature setpoint."""
        temp_set: float | None = None
        mode = self.get_mode()
        if mode is not None:
            if mode.is_cool():
                temp_set = self.get_temp_set_cool_air()
            elif mode.is_dry():
                temp_set = self.get_temp_set_dry_air()
            elif mode.is_heat():
                temp_set = self.get_temp_set_hot_air()
            elif mode.is_stop():
                temp_set = self.get_temp_set_stop_air()
            elif mode.is_vent():
                temp_set = self.get_temp_set_vent_air()
        return temp_set

    def get_temp_set_cool_air(self) -> float | None:
        """Return HVAC device setpoint for Cool Air."""
        if self.temp_set_cool_air is not None:
            return round(self.temp_set_cool_air, 1)
        return None

    def get_temp_set_dry_air(self) -> float | None:
        """Return HVAC device setpoint for Dry Air."""
        if self.temp_set_dry_air is not None:
            return round(self.temp_set_dry_air, 1)
        return None

    def get_temp_set_hot_air(self) -> float | None:
        """Return HVAC device setpoint for Heat Air."""
        if self.temp_set_hot_air is not None:
            return round(self.temp_set_hot_air, 1)
        return None

    def get_temp_set_stop_air(self) -> float | None:
        """Return HVAC device setpoint for Stop Air."""
        if self.temp_set_stop_air is not None:
            return round(self.temp_set_stop_air, 1)
        return None

    def get_temp_set_vent_air(self) -> float | None:
        """Return HVAC device setpoint for Ventilation Air."""
        if self.temp_set_vent_air is not None:
            return round(self.temp_set_vent_air, 1)
        return None

    def get_temp_set_max(self) -> float | None:
        """Return HVAC device max setpoint."""
        max_temp: float | None = None
        temps = [
            self.get_temp_set_max_cool_air(),
            self.get_temp_set_max_dry_air(),
            self.get_temp_set_max_emerheat_air(),
            self.get_temp_set_max_hot_air(),
            self.get_temp_set_max_stop_air(),
            self.get_temp_set_max_vent_air(),
        ]
        for temp in temps:
            if temp is not None:
                if max_temp is None or temp > max_temp:
                    max_temp = temp
        return max_temp

    def get_temp_set_max_cool_air(self) -> float | None:
        """Return HVAC device max setpoint for Cool Air."""
        if self.temp_set_max_cool_air is not None:
            return round(self.temp_set_max_cool_air, 1)
        return None

    def get_temp_set_max_dry_air(self) -> float | None:
        """Return HVAC device max setpoint for Dry Air."""
        if self.temp_set_max_dry_air is not None:
            return round(self.temp_set_max_dry_air, 1)
        return None

    def get_temp_set_max_emerheat_air(self) -> float | None:
        """Return HVAC device max setpoint for Emergency Heat Air."""
        if self.temp_set_max_emerheat_air is not None:
            return round(self.temp_set_max_emerheat_air, 1)
        return None

    def get_temp_set_max_hot_air(self) -> float | None:
        """Return HVAC device max setpoint for Heat Air."""
        if self.temp_set_max_hot_air is not None:
            return round(self.temp_set_max_hot_air, 1)
        return None

    def get_temp_set_max_stop_air(self) -> float | None:
        """Return HVAC device max setpoint for Stop Air."""
        if self.temp_set_max_stop_air is not None:
            return round(self.temp_set_max_stop_air, 1)
        return None

    def get_temp_set_max_vent_air(self) -> float | None:
        """Return HVAC device max setpoint for Ventilation Air."""
        if self.temp_set_max_vent_air is not None:
            return round(self.temp_set_max_vent_air, 1)
        return None

    def get_temp_set_min(self) -> float | None:
        """Return HVAC device min setpoint."""
        min_temp: float | None = None
        temps = [
            self.get_temp_set_min_cool_air(),
            self.get_temp_set_min_dry_air(),
            self.get_temp_set_min_emerheat_air(),
            self.get_temp_set_min_hot_air(),
            self.get_temp_set_min_stop_air(),
            self.get_temp_set_min_vent_air(),
        ]
        for temp in temps:
            if temp is not None:
                if min_temp is None or temp < min_temp:
                    min_temp = temp
        return min_temp

    def get_temp_set_min_cool_air(self) -> float | None:
        """Return HVAC device min setpoint for Cool Air."""
        if self.temp_set_min_cool_air:
            return round(self.temp_set_min_cool_air, 1)
        return None

    def get_temp_set_min_dry_air(self) -> float | None:
        """Return HVAC device min setpoint for Dry Air."""
        if self.temp_set_min_dry_air is not None:
            return round(self.temp_set_min_dry_air, 1)
        return None

    def get_temp_set_min_emerheat_air(self) -> float | None:
        """Return HVAC device min setpoint for Emergency Heat Air."""
        if self.temp_set_min_emerheat_air is not None:
            return round(self.temp_set_min_emerheat_air, 1)
        return None

    def get_temp_set_min_hot_air(self) -> float | None:
        """Return HVAC device min setpoint for Hot Air."""
        if self.temp_set_min_hot_air is not None:
            return round(self.temp_set_min_hot_air, 1)
        return None

    def get_temp_set_min_stop_air(self) -> float | None:
        """Return HVAC device min setpoint for Stop Air."""
        if self.temp_set_min_stop_air is not None:
            return round(self.temp_set_min_stop_air, 1)
        return None

    def get_temp_set_min_vent_air(self) -> float | None:
        """Return HVAC device min setpoint for Ventilation Air."""
        if self.temp_set_min_vent_air is not None:
            return round(self.temp_set_min_vent_air, 1)
        return None

    def get_temp_step(self) -> float | None:
        """Return HVAC device temperature step."""
        if self.temp_step is not None:
            return round(self.temp_step, 1)
        return API_DEFAULT_TEMP_STEP

    def update(self, data: dict[str, Any]) -> None:
        """Update HVAC device data."""
        super().update(data)

        if API_ACTIVE in data:
            self.active = bool(data[API_ACTIVE])

        if API_HUMIDITY in data:
            self.humidity = int(data[API_HUMIDITY])

        if API_LOCAL_TEMP in data:
            if API_CELSIUS in data[API_LOCAL_TEMP]:
                self.temp = float(data[API_LOCAL_TEMP][API_CELSIUS])

        if API_POWER in data:
            self.power = bool(data[API_POWER])

        if API_RANGE_SP_MAX_COOL_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MAX_COOL_AIR]:
                self.temp_set_max_cool_air = float(
                    data[API_RANGE_SP_MAX_COOL_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MAX_DRY_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MAX_DRY_AIR]:
                self.temp_set_max_dry_air = float(
                    data[API_RANGE_SP_MAX_DRY_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MAX_EMERHEAT_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MAX_EMERHEAT_AIR]:
                self.temp_set_max_emerheat_air = float(
                    data[API_RANGE_SP_MAX_EMERHEAT_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MAX_HOT_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MAX_HOT_AIR]:
                self.temp_set_max_hot_air = float(
                    data[API_RANGE_SP_MAX_HOT_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MAX_STOP_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MAX_STOP_AIR]:
                self.temp_set_max_stop_air = float(
                    data[API_RANGE_SP_MAX_STOP_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MAX_VENT_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MAX_VENT_AIR]:
                self.temp_set_max_vent_air = float(
                    data[API_RANGE_SP_MAX_VENT_AIR][API_CELSIUS]
                )

        if API_RANGE_SP_MIN_COOL_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MIN_COOL_AIR]:
                self.temp_set_min_cool_air = float(
                    data[API_RANGE_SP_MIN_COOL_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MIN_DRY_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MIN_DRY_AIR]:
                self.temp_set_min_dry_air = float(
                    data[API_RANGE_SP_MIN_DRY_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MIN_EMERHEAT_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MIN_EMERHEAT_AIR]:
                self.temp_set_min_emerheat_air = float(
                    data[API_RANGE_SP_MIN_EMERHEAT_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MIN_HOT_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MIN_HOT_AIR]:
                self.temp_set_min_hot_air = float(
                    data[API_RANGE_SP_MIN_HOT_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MIN_STOP_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MIN_STOP_AIR]:
                self.temp_set_min_stop_air = float(
                    data[API_RANGE_SP_MIN_STOP_AIR][API_CELSIUS]
                )
        if API_RANGE_SP_MIN_VENT_AIR in data:
            if API_CELSIUS in data[API_RANGE_SP_MIN_VENT_AIR]:
                self.temp_set_min_vent_air = float(
                    data[API_RANGE_SP_MIN_VENT_AIR][API_CELSIUS]
                )

        if API_SP_AIR_COOL in data:
            if API_CELSIUS in data[API_SP_AIR_COOL]:
                self.temp_set_cool_air = float(data[API_SP_AIR_COOL][API_CELSIUS])
        if API_SP_AIR_DRY in data:
            if API_CELSIUS in data[API_SP_AIR_DRY]:
                self.temp_set_dry_air = float(data[API_SP_AIR_DRY][API_CELSIUS])
        if API_SP_AIR_HEAT in data:
            if API_CELSIUS in data[API_SP_AIR_HEAT]:
                self.temp_set_hot_air = float(data[API_SP_AIR_HEAT][API_CELSIUS])
        if API_SP_AIR_STOP in data:
            if API_CELSIUS in data[API_SP_AIR_STOP]:
                self.temp_set_stop_air = float(data[API_SP_AIR_STOP][API_CELSIUS])
        if API_SP_AIR_VENT in data:
            if API_CELSIUS in data[API_SP_AIR_VENT]:
                self.temp_set_vent_air = float(data[API_SP_AIR_VENT][API_CELSIUS])

        if API_STEP in data:
            if API_CELSIUS in data[API_STEP]:
                self.temp_step = float(data[API_STEP][API_CELSIUS])
