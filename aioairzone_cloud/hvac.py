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
    API_RANGE_MAX_AIR,
    API_RANGE_MIN_AIR,
    API_RANGE_SP_MAX_AUTO_AIR,
    API_RANGE_SP_MAX_COOL_AIR,
    API_RANGE_SP_MAX_DRY_AIR,
    API_RANGE_SP_MAX_EMERHEAT_AIR,
    API_RANGE_SP_MAX_HOT_AIR,
    API_RANGE_SP_MAX_STOP_AIR,
    API_RANGE_SP_MAX_VENT_AIR,
    API_RANGE_SP_MIN_AUTO_AIR,
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
    AZD_TEMP_SET_AUTO_AIR,
    AZD_TEMP_SET_COOL_AIR,
    AZD_TEMP_SET_DRY_AIR,
    AZD_TEMP_SET_HOT_AIR,
    AZD_TEMP_SET_MAX,
    AZD_TEMP_SET_MAX_AUTO_AIR,
    AZD_TEMP_SET_MAX_COOL_AIR,
    AZD_TEMP_SET_MAX_DRY_AIR,
    AZD_TEMP_SET_MAX_EMERHEAT_AIR,
    AZD_TEMP_SET_MAX_HOT_AIR,
    AZD_TEMP_SET_MAX_STOP_AIR,
    AZD_TEMP_SET_MAX_VENT_AIR,
    AZD_TEMP_SET_MIN,
    AZD_TEMP_SET_MIN_AUTO_AIR,
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
        self.temp_set_max: float | None = None
        self.temp_set_max_auto_air: float | None = None
        self.temp_set_max_cool_air: float | None = None
        self.temp_set_max_dry_air: float | None = None
        self.temp_set_max_emerheat_air: float | None = None
        self.temp_set_max_hot_air: float | None = None
        self.temp_set_max_stop_air: float | None = None
        self.temp_set_max_vent_air: float | None = None
        self.temp_set_min: float | None = None
        self.temp_set_min_auto_air: float | None = None
        self.temp_set_min_cool_air: float | None = None
        self.temp_set_min_dry_air: float | None = None
        self.temp_set_min_emerheat_air: float | None = None
        self.temp_set_min_hot_air: float | None = None
        self.temp_set_min_stop_air: float | None = None
        self.temp_set_min_vent_air: float | None = None
        self.temp_set_auto_air: float | None = None
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
        temp_set_max_auto_air = self.get_temp_set_max_auto_air()
        if temp_set_max_auto_air is not None:
            data[AZD_TEMP_SET_MAX_AUTO_AIR] = temp_set_max_auto_air
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
        temp_set_min_auto_air = self.get_temp_set_min_auto_air()
        if temp_set_min_auto_air is not None:
            data[AZD_TEMP_SET_MIN_AUTO_AIR] = temp_set_min_auto_air
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
        temp_set_auto_air = self.get_temp_set_auto_air()
        if temp_set_auto_air is not None:
            data[AZD_TEMP_SET_AUTO_AIR] = temp_set_auto_air
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
                    action = self.get_action_auto()
                else:
                    action = OperationAction.OFF
            else:
                action = OperationAction.IDLE
        else:
            action = OperationAction.OFF
        return action

    def get_action_auto(self) -> OperationAction:
        """Return current Auto action."""
        mode = self.get_mode_auto()
        if mode is not None:
            if mode.is_cool():
                action = OperationAction.COOLING
            elif mode.is_heat():
                action = OperationAction.HEATING
            elif mode.is_vent():
                action = OperationAction.FAN
            elif mode.is_dry():
                action = OperationAction.DRYING
            else:
                action = OperationAction.IDLE
        else:
            action = OperationAction.IDLE
        return action

    def get_active(self) -> bool | None:
        """Return HVAC device active status."""
        return self.active

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
            if mode.is_auto():
                temp_set = self.get_temp_set_auto_air()
            elif mode.is_cool():
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

    def get_temp_set_auto_air(self) -> float | None:
        """Return HVAC device setpoint for Auto Air."""
        if self.temp_set_auto_air is not None:
            return round(self.temp_set_auto_air, 1)
        return None

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
            self.temp_set_max,
            self.get_temp_set_max_auto_air(),
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

    def get_temp_set_max_auto_air(self) -> float | None:
        """Return HVAC device max setpoint for Auto Air."""
        if self.temp_set_max_auto_air is not None:
            return round(self.temp_set_max_auto_air, 1)
        return None

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
            self.temp_set_min,
            self.get_temp_set_min_auto_air(),
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

    def get_temp_set_min_auto_air(self) -> float | None:
        """Return HVAC device min setpoint for Auto Air."""
        if self.temp_set_min_auto_air:
            return round(self.temp_set_min_auto_air, 1)
        return None

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

    def set_power(self, power: bool) -> None:
        """Set HVAC power."""
        self.power = power

    def set_setpoint(self, setpoint: float) -> None:
        """Set HVAC setpoint."""
        if self.temp_set_auto_air is not None:
            self.temp_set_auto_air = setpoint
        if self.temp_set_cool_air is not None:
            self.temp_set_cool_air = setpoint
        if self.temp_set_dry_air is not None:
            self.temp_set_dry_air = setpoint
        if self.temp_set_hot_air is not None:
            self.temp_set_hot_air = setpoint
        if self.temp_set_stop_air is not None:
            self.temp_set_stop_air = setpoint
        if self.temp_set_vent_air is not None:
            self.temp_set_vent_air = setpoint

    def update(self, data: dict[str, Any]) -> None:
        """Update HVAC device data."""
        super().update(data)

        active = data.get(API_ACTIVE)
        if active is not None:
            self.active = bool(active)

        humidity = data.get(API_HUMIDITY)
        if humidity is not None:
            self.humidity = int(humidity)

        local_temp = data.get(API_LOCAL_TEMP)
        if local_temp is not None:
            if API_CELSIUS in local_temp:
                self.temp = float(local_temp[API_CELSIUS])

        power = data.get(API_POWER)
        if power is not None:
            self.power = bool(power)

        range_max_air = data.get(API_RANGE_MAX_AIR)
        if range_max_air is not None:
            if API_CELSIUS in range_max_air:
                self.temp_set_max = float(range_max_air[API_CELSIUS])
        range_sp_max_auto_air = data.get(API_RANGE_SP_MAX_AUTO_AIR)
        if range_sp_max_auto_air is not None:
            if API_CELSIUS in range_sp_max_auto_air:
                self.temp_set_max_auto_air = float(range_sp_max_auto_air[API_CELSIUS])
        range_sp_max_cool_air = data.get(API_RANGE_SP_MAX_COOL_AIR)
        if range_sp_max_cool_air is not None:
            if API_CELSIUS in range_sp_max_cool_air:
                self.temp_set_max_cool_air = float(range_sp_max_cool_air[API_CELSIUS])
        range_sp_max_dry_air = data.get(API_RANGE_SP_MAX_DRY_AIR)
        if range_sp_max_dry_air is not None:
            if API_CELSIUS in range_sp_max_dry_air:
                self.temp_set_max_dry_air = float(range_sp_max_dry_air[API_CELSIUS])
        range_sp_max_emerheat_air = data.get(API_RANGE_SP_MAX_EMERHEAT_AIR)
        if range_sp_max_emerheat_air is not None:
            if API_CELSIUS in range_sp_max_emerheat_air:
                self.temp_set_max_emerheat_air = float(
                    range_sp_max_emerheat_air[API_CELSIUS]
                )
        range_sp_max_hot_air = data.get(API_RANGE_SP_MAX_HOT_AIR)
        if range_sp_max_hot_air is not None:
            if API_CELSIUS in range_sp_max_hot_air:
                self.temp_set_max_hot_air = float(range_sp_max_hot_air[API_CELSIUS])
        range_sp_max_stop_air = data.get(API_RANGE_SP_MAX_STOP_AIR)
        if range_sp_max_stop_air is not None:
            if API_CELSIUS in range_sp_max_stop_air:
                self.temp_set_max_stop_air = float(range_sp_max_stop_air[API_CELSIUS])
        range_sp_max_vent_air = data.get(API_RANGE_SP_MAX_VENT_AIR)
        if range_sp_max_vent_air is not None:
            if API_CELSIUS in range_sp_max_vent_air:
                self.temp_set_max_vent_air = float(range_sp_max_vent_air[API_CELSIUS])

        range_min_air = data.get(API_RANGE_MIN_AIR)
        if range_min_air is not None:
            if API_CELSIUS in range_min_air:
                self.temp_set_min = float(range_min_air[API_CELSIUS])
        range_sp_min_auto_air = data.get(API_RANGE_SP_MIN_AUTO_AIR)
        if range_sp_min_auto_air is not None:
            if API_CELSIUS in range_sp_min_auto_air:
                self.temp_set_min_auto_air = float(range_sp_min_auto_air[API_CELSIUS])
        range_sp_min_cool_air = data.get(API_RANGE_SP_MIN_COOL_AIR)
        if range_sp_min_cool_air is not None:
            if API_CELSIUS in range_sp_min_cool_air:
                self.temp_set_min_cool_air = float(range_sp_min_cool_air[API_CELSIUS])
        range_sp_min_dry_air = data.get(API_RANGE_SP_MIN_DRY_AIR)
        if range_sp_min_dry_air is not None:
            if API_CELSIUS in range_sp_min_dry_air:
                self.temp_set_min_dry_air = float(range_sp_min_dry_air[API_CELSIUS])
        range_sp_min_emerheat_air = data.get(API_RANGE_SP_MIN_EMERHEAT_AIR)
        if range_sp_min_emerheat_air is not None:
            if API_CELSIUS in range_sp_min_emerheat_air:
                self.temp_set_min_emerheat_air = float(
                    range_sp_min_emerheat_air[API_CELSIUS]
                )
        range_sp_min_hot_air = data.get(API_RANGE_SP_MIN_HOT_AIR)
        if range_sp_min_hot_air is not None:
            if API_CELSIUS in range_sp_min_hot_air:
                self.temp_set_min_hot_air = float(range_sp_min_hot_air[API_CELSIUS])
        range_sp_min_stop_air = data.get(API_RANGE_SP_MIN_STOP_AIR)
        if range_sp_min_stop_air is not None:
            if API_CELSIUS in range_sp_min_stop_air:
                self.temp_set_min_stop_air = float(range_sp_min_stop_air[API_CELSIUS])
        range_sp_min_vent_air = data.get(API_RANGE_SP_MIN_VENT_AIR)
        if range_sp_min_vent_air is not None:
            if API_CELSIUS in range_sp_min_vent_air:
                self.temp_set_min_vent_air = float(range_sp_min_vent_air[API_CELSIUS])

        sp_air_cool = data.get(API_SP_AIR_COOL)
        if sp_air_cool is not None:
            if API_CELSIUS in sp_air_cool:
                self.temp_set_cool_air = float(sp_air_cool[API_CELSIUS])
        sp_air_dry = data.get(API_SP_AIR_DRY)
        if sp_air_dry is not None:
            if API_CELSIUS in sp_air_dry:
                self.temp_set_dry_air = float(data[API_SP_AIR_DRY][API_CELSIUS])
        sp_air_heat = data.get(API_SP_AIR_HEAT)
        if sp_air_heat is not None:
            if API_CELSIUS in sp_air_heat:
                self.temp_set_hot_air = float(sp_air_heat[API_CELSIUS])
        sp_air_stop = data.get(API_SP_AIR_STOP)
        if sp_air_stop is not None:
            if API_CELSIUS in sp_air_stop:
                self.temp_set_stop_air = float(sp_air_stop[API_CELSIUS])
        sp_air_vent = data.get(API_SP_AIR_VENT)
        if sp_air_vent is not None:
            if API_CELSIUS in sp_air_vent:
                self.temp_set_vent_air = float(sp_air_vent[API_CELSIUS])

        step = data.get(API_STEP)
        if step is not None:
            if API_CELSIUS in step:
                self.temp_step = float(step[API_CELSIUS])
