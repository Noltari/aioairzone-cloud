"""Airzone Cloud API HVAC device."""

from __future__ import annotations

from typing import Any

from .common import (
    AirQualityMode,
    OperationAction,
    OperationMode,
    SpeedType,
    parse_bool,
    parse_float,
    parse_int,
)
from .const import (
    API_ACTIVE,
    API_AIR_ACTIVE,
    API_AQ_ACTIVE,
    API_AQ_MODE_CONF,
    API_AQ_MODE_VALUES,
    API_CELSIUS,
    API_DEFAULT_TEMP_STEP,
    API_DOUBLE_SET_POINT,
    API_HUMIDITY,
    API_LOCAL_TEMP,
    API_POWER,
    API_RAD_ACTIVE,
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
    API_SPEED_CONF,
    API_SPEED_TYPE,
    API_SPEED_VALUES,
    API_STEP,
    AZD_ACTION,
    AZD_ACTIVE,
    AZD_AIR_DEMAND,
    AZD_AQ_ACTIVE,
    AZD_AQ_MODE_CONF,
    AZD_AQ_MODE_VALUES,
    AZD_DOUBLE_SET_POINT,
    AZD_FLOOR_DEMAND,
    AZD_HUMIDITY,
    AZD_POWER,
    AZD_SPEED,
    AZD_SPEED_TYPE,
    AZD_SPEEDS,
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
from .entity import EntityUpdate, UpdateType


class HVAC(Device):
    """Airzone Cloud HVAC device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud HVAC device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.active: bool | None = None
        self.air_demand: bool | None = None
        self.aq_active: bool | None = None
        self.aq_mode_conf: AirQualityMode | None = None
        self.aq_mode_values: list[AirQualityMode] | None = None
        self.double_set_point: bool | None = None
        self.humidity: int | None = None
        self.floor_demand: bool | None = None
        self.name: str = "HVAC"
        self.power: bool | None = None
        self.speed: int | None = None
        self.speeds: dict[int, int] = {}
        self.speed_type: SpeedType | None = None
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
        data[AZD_DOUBLE_SET_POINT] = self.get_double_set_point()
        data[AZD_POWER] = self.get_power()
        data[AZD_TEMP] = self.get_temperature()
        data[AZD_TEMP_STEP] = self.get_temp_step()

        air_demand = self.get_air_demand()
        if air_demand is not None:
            data[AZD_AIR_DEMAND] = air_demand
        floor_demand = self.get_floor_demand()
        if floor_demand is not None:
            data[AZD_FLOOR_DEMAND] = floor_demand

        aq_active = self.get_aq_active()
        if aq_active is not None:
            data[AZD_AQ_ACTIVE] = aq_active

        aq_mode_conf = self.get_aq_mode_conf()
        if aq_mode_conf is not None:
            data[AZD_AQ_MODE_CONF] = aq_mode_conf

        aq_mode_values = self.get_aq_mode_values()
        if aq_mode_values is not None:
            data[AZD_AQ_MODE_VALUES] = aq_mode_values

        humidity = self.get_humidity()
        if humidity is not None:
            data[AZD_HUMIDITY] = humidity

        speed = self.get_speed()
        if speed is not None:
            data[AZD_SPEED] = speed

        speeds = self.get_speeds()
        if speeds is not None:
            data[AZD_SPEEDS] = speeds

        speed_type = self.get_speed_type()
        if speed_type is not None:
            data[AZD_SPEED_TYPE] = speed_type

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

    def get_air_demand(self) -> bool | None:
        """Return HVAC device air_demand status."""
        return self.air_demand

    def get_aq_active(self) -> bool | None:
        """Return HVAC device Air Quality active status."""
        return self.aq_active

    def get_aq_mode_conf(self) -> AirQualityMode | None:
        """Return HVAC device Air Quality mode conf."""
        return self.aq_mode_conf

    def get_aq_mode_values(self) -> list[AirQualityMode] | None:
        """Return HVAC device Air Quality mode values."""
        if self.aq_mode_values is not None and len(self.aq_mode_values) > 0:
            return self.aq_mode_values
        return None

    def get_double_set_point(self) -> bool:
        """Return HVAC double set point."""
        if self.double_set_point is not None:
            return self.double_set_point
        return False

    def get_floor_demand(self) -> bool | None:
        """Return HVAC device floor demand status."""
        return self.floor_demand

    def get_humidity(self) -> int | None:
        """Return HVAC device humidity."""
        return self.humidity

    def get_power(self) -> bool | None:
        """Return HVAC device power."""
        return self.power

    def get_speed(self) -> int | None:
        """Return HVAC speed."""
        return self.speed

    def get_speeds(self) -> dict[int, int] | None:
        """Return HVAC speeds."""
        if len(self.speeds) > 0:
            return self.speeds
        return None

    def get_speed_type(self) -> SpeedType | None:
        """Return HVAC speed type."""
        return self.speed_type

    def set_speed(self, speed: int) -> None:
        """Set HVAC speed."""
        if self.speed is not None:
            self.speed = speed

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

    def set_aq_mode(self, aq_mode: AirQualityMode) -> None:
        """Set HVAC Air Quality mode."""
        self.aq_mode_conf = aq_mode

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

    def set_setpoint_cool(self, setpoint: float) -> None:
        """Set HVAC cool setpoint."""
        if self.temp_set_cool_air is not None:
            self.temp_set_cool_air = setpoint

    def set_setpoint_heat(self, setpoint: float) -> None:
        """Set HVAC heat setpoint."""
        if self.temp_set_hot_air is not None:
            self.temp_set_hot_air = setpoint

    def update_data(self, update: EntityUpdate) -> None:
        """Update HVAC device data."""
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

        if API_AIR_ACTIVE in data:
            air_demand = parse_bool(data.get(API_AIR_ACTIVE))
            if air_demand is not None:
                self.air_demand = air_demand
            else:
                # API sends API_AIR_ACTIVE as null instead of False
                self.air_demand = False
        else:
            if update.get_type() != UpdateType.WS_PARTIAL:
                self.air_demand = None

        if API_RAD_ACTIVE in data:
            floor_demand = parse_bool(data.get(API_RAD_ACTIVE))
            if floor_demand is not None:
                self.floor_demand = floor_demand
            else:
                # API sends API_RAD_ACTIVE as null instead of False
                self.floor_demand = False
        else:
            if update.get_type() != UpdateType.WS_PARTIAL:
                self.floor_demand = None

        aq_active = parse_bool(data.get(API_AQ_ACTIVE))
        if aq_active is not None:
            self.aq_active = aq_active

        aq_mode_conf = data.get(API_AQ_MODE_CONF)
        if aq_mode_conf is not None:
            self.aq_mode_conf = AirQualityMode(aq_mode_conf)

        aq_mode_values = data.get(API_AQ_MODE_VALUES)
        if aq_mode_values is not None:
            self.aq_mode_values = []
            for aq_mode_value in aq_mode_values:
                self.aq_mode_values += [AirQualityMode(aq_mode_value)]

        double_set_point = parse_bool(data.get(API_DOUBLE_SET_POINT))
        if double_set_point is not None:
            self.double_set_point = double_set_point

        humidity = parse_int(data.get(API_HUMIDITY))
        if humidity is not None:
            self.humidity = humidity

        local_temp = parse_float(data.get(API_LOCAL_TEMP, {}).get(API_CELSIUS))
        if local_temp is not None:
            self.temp = local_temp

        power = parse_bool(data.get(API_POWER))
        if power is not None:
            self.power = power

        range_max_air = parse_float(data.get(API_RANGE_MAX_AIR, {}).get(API_CELSIUS))
        if range_max_air is not None:
            self.temp_set_max = range_max_air
        range_sp_max_auto_air = parse_float(
            data.get(API_RANGE_SP_MAX_AUTO_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_max_auto_air is not None:
            self.temp_set_max_auto_air = range_sp_max_auto_air
        range_sp_max_cool_air = parse_float(
            data.get(API_RANGE_SP_MAX_COOL_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_max_cool_air is not None:
            self.temp_set_max_cool_air = range_sp_max_cool_air
        range_sp_max_dry_air = parse_float(
            data.get(API_RANGE_SP_MAX_DRY_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_max_dry_air is not None:
            self.temp_set_max_dry_air = range_sp_max_dry_air
        range_sp_max_emerheat_air = parse_float(
            data.get(API_RANGE_SP_MAX_EMERHEAT_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_max_emerheat_air is not None:
            self.temp_set_max_emerheat_air = range_sp_max_emerheat_air
        range_sp_max_hot_air = parse_float(
            data.get(API_RANGE_SP_MAX_HOT_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_max_hot_air is not None:
            self.temp_set_max_hot_air = range_sp_max_hot_air
        range_sp_max_stop_air = parse_float(
            data.get(API_RANGE_SP_MAX_STOP_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_max_stop_air is not None:
            self.temp_set_max_stop_air = range_sp_max_stop_air
        range_sp_max_vent_air = parse_float(
            data.get(API_RANGE_SP_MAX_VENT_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_max_vent_air is not None:
            self.temp_set_max_vent_air = range_sp_max_vent_air

        range_min_air = parse_float(data.get(API_RANGE_MIN_AIR, {}).get(API_CELSIUS))
        if range_min_air is not None:
            self.temp_set_min = range_min_air
        range_sp_min_auto_air = parse_float(
            data.get(API_RANGE_SP_MIN_AUTO_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_min_auto_air is not None:
            self.temp_set_min_auto_air = range_sp_min_auto_air
        range_sp_min_cool_air = parse_float(
            data.get(API_RANGE_SP_MIN_COOL_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_min_cool_air is not None:
            self.temp_set_min_cool_air = range_sp_min_cool_air
        range_sp_min_dry_air = parse_float(
            data.get(API_RANGE_SP_MIN_DRY_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_min_dry_air is not None:
            self.temp_set_min_dry_air = range_sp_min_dry_air
        range_sp_min_emerheat_air = parse_float(
            data.get(API_RANGE_SP_MIN_EMERHEAT_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_min_emerheat_air is not None:
            self.temp_set_min_emerheat_air = range_sp_min_emerheat_air
        range_sp_min_hot_air = parse_float(
            data.get(API_RANGE_SP_MIN_HOT_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_min_hot_air is not None:
            self.temp_set_min_hot_air = range_sp_min_hot_air
        range_sp_min_stop_air = parse_float(
            data.get(API_RANGE_SP_MIN_STOP_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_min_stop_air is not None:
            self.temp_set_min_stop_air = range_sp_min_stop_air
        range_sp_min_vent_air = parse_float(
            data.get(API_RANGE_SP_MIN_VENT_AIR, {}).get(API_CELSIUS)
        )
        if range_sp_min_vent_air is not None:
            self.temp_set_min_vent_air = range_sp_min_vent_air

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

        sp_air_cool = parse_float(data.get(API_SP_AIR_COOL, {}).get(API_CELSIUS))
        if sp_air_cool is not None:
            self.temp_set_cool_air = sp_air_cool
        sp_air_dry = parse_float(data.get(API_SP_AIR_DRY, {}).get(API_CELSIUS))
        if sp_air_dry is not None:
            self.temp_set_dry_air = sp_air_dry
        sp_air_heat = parse_float(data.get(API_SP_AIR_HEAT, {}).get(API_CELSIUS))
        if sp_air_heat is not None:
            self.temp_set_hot_air = sp_air_heat
        sp_air_stop = parse_float(data.get(API_SP_AIR_STOP, {}).get(API_CELSIUS))
        if sp_air_stop is not None:
            self.temp_set_stop_air = sp_air_stop
        sp_air_vent = parse_float(data.get(API_SP_AIR_VENT, {}).get(API_CELSIUS))
        if sp_air_vent is not None:
            self.temp_set_vent_air = sp_air_vent

        step = parse_float(data.get(API_STEP, {}).get(API_CELSIUS))
        if step is not None:
            self.temp_step = step
