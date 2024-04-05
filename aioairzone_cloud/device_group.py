"""Airzone Cloud API Device."""

from __future__ import annotations

from abc import ABC
from collections import Counter
from typing import Any

from .aidoo import Aidoo
from .common import OperationAction, OperationMode
from .const import (
    API_DEFAULT_TEMP_STEP,
    API_PARAMS,
    API_VALUE,
    AZD_ACTION,
    AZD_ACTIVE,
    AZD_AIDOOS,
    AZD_AVAILABLE,
    AZD_HOT_WATERS,
    AZD_HUMIDITY,
    AZD_ID,
    AZD_MODE,
    AZD_MODES,
    AZD_NAME,
    AZD_NUM_DEVICES,
    AZD_POWER,
    AZD_SYSTEMS,
    AZD_TEMP,
    AZD_TEMP_SET,
    AZD_TEMP_SET_MAX,
    AZD_TEMP_SET_MIN,
    AZD_TEMP_STEP,
    AZD_ZONES,
)
from .hotwater import HotWater
from .system import System
from .zone import Zone


class DeviceGroup(ABC):
    """Airzone Cloud DeviceGroup."""

    id: str
    name: str

    def __init__(self) -> None:
        """Airzone Cloud DeviceGroup init."""

        self.aidoos: dict[str, Aidoo] = {}
        self.dhws: dict[str, HotWater] = {}
        self.systems: dict[str, System] = {}
        self.zones: dict[str, Zone] = {}

    def data(self) -> dict[str, Any]:
        """Return DeviceGroup data."""
        data: dict[str, Any] = {}

        if len(self.aidoos) > 0:
            data[AZD_AIDOOS] = list(self.aidoos)
        if len(self.dhws) > 0:
            data[AZD_HOT_WATERS] = list(self.dhws)
        if len(self.systems) > 0:
            data[AZD_SYSTEMS] = list(self.systems)
        if len(self.zones) > 0:
            data[AZD_ZONES] = list(self.zones)

        data[AZD_ACTION] = self.get_action()
        data[AZD_ACTIVE] = self.get_active()
        data[AZD_AVAILABLE] = self.get_available()
        data[AZD_ID] = self.get_id()
        data[AZD_MODE] = self.get_mode()
        data[AZD_NAME] = self.get_name()
        data[AZD_NUM_DEVICES] = self.get_devices_num()
        data[AZD_POWER] = self.get_power()
        data[AZD_TEMP] = self.get_temperature()
        data[AZD_TEMP_STEP] = self.get_temp_step()

        humidity = self.get_humidity()
        if humidity is not None:
            data[AZD_HUMIDITY] = humidity

        modes = self.get_modes()
        if modes is not None:
            data[AZD_MODES] = modes

        temp_set_max = self.get_temp_set_max()
        if temp_set_max is not None:
            data[AZD_TEMP_SET_MAX] = temp_set_max

        temp_set_min = self.get_temp_set_min()
        if temp_set_min is not None:
            data[AZD_TEMP_SET_MIN] = temp_set_min

        temp_set = self.get_temp_set()
        if temp_set is not None:
            data[AZD_TEMP_SET] = temp_set

        return data

    def get_action(self) -> OperationAction:
        """Return DeviceGroup action."""
        action_values: list[OperationAction] = []
        for aidoo in self.aidoos.values():
            action_values += [aidoo.get_action()]
        for zone in self.zones.values():
            action_values += [zone.get_action()]
        if len(action_values) > 0:
            action_cnt = Counter(action_values)
            idle_cnt = action_cnt[OperationAction.IDLE]
            del action_cnt[OperationAction.IDLE]
            del action_cnt[OperationAction.OFF]
            action_mc = action_cnt.most_common(1)
            if len(action_mc) > 0:
                return action_mc[0][0]
            if idle_cnt > 0:
                return OperationAction.IDLE
        return OperationAction.OFF

    def get_active(self) -> bool | None:
        """Return DeviceGroup active status."""
        active_values: list[bool] = []
        for aidoo in self.aidoos.values():
            active = aidoo.get_active()
            if active is not None:
                active_values += [active]
        for zone in self.zones.values():
            active = zone.get_active()
            if active is not None:
                active_values += [active]
        if len(active_values) > 0:
            if True in active_values:
                return True
            if False in active_values:
                return False
        return None

    def add_aidoo(self, aidoo: Aidoo) -> None:
        """Add Aidoo to DeviceGroup."""
        aidoo_id = aidoo.get_id()
        if aidoo_id not in self.aidoos:
            self.aidoos[aidoo_id] = aidoo

    def add_dhw(self, dhw: HotWater) -> None:
        """Add DHW to DeviceGroup."""
        dhw_id = dhw.get_id()
        if dhw_id not in self.dhws:
            self.dhws[dhw_id] = dhw

    def add_system(self, system: System) -> None:
        """Add System to DeviceGroup."""
        system_id = system.get_id()
        if system_id not in self.systems:
            self.systems[system_id] = system

    def add_zone(self, zone: Zone) -> None:
        """Add Zone to DeviceGroup."""
        zone_id = zone.get_id()
        if zone_id not in self.zones:
            self.zones[zone_id] = zone

    def get_available(self) -> bool:
        """Return DeviceGroup availability status."""
        for aidoo in self.aidoos.values():
            if aidoo.get_available():
                return True
        for zone in self.zones.values():
            if zone.get_available():
                return True
        return False

    def get_devices_num(self) -> int:
        """Return DeviceGroup devices count."""
        return len(self.aidoos) + len(self.zones)

    def get_humidity(self) -> int | None:
        """Return DeviceGroup humidity."""
        humidity: int | float | None
        humidity_values: list[int] = []
        for aidoo in self.aidoos.values():
            humidity = aidoo.get_humidity()
            if humidity is not None:
                humidity_values += [humidity]
        for zone in self.zones.values():
            humidity = zone.get_humidity()
            if humidity is not None:
                humidity_values += [humidity]
        if len(humidity_values) > 0:
            humidity = sum(humidity_values) / len(humidity_values)
            return int(humidity)
        return None

    def get_id(self) -> str:
        """Return DeviceGroup ID."""
        return self.id

    def get_mode(self) -> OperationMode | None:
        """Return DeviceGroup mode."""
        mode_values: list[OperationMode] = []
        for aidoo in self.aidoos.values():
            mode = aidoo.get_mode()
            if mode is not None:
                mode_values += [mode]
        for zone in self.zones.values():
            mode = zone.get_mode()
            if mode is not None:
                mode_values += [mode]
        if len(mode_values) > 0:
            mode_cnt = Counter(mode_values)
            del mode_cnt[OperationMode.STOP]
            mode_mc = mode_cnt.most_common(1)
            if len(mode_mc) > 0:
                return mode_mc[0][0]
        return OperationMode.STOP

    def get_modes(self) -> list[OperationMode] | None:
        """Return DeviceGroup modes."""
        mode_values: list[OperationMode] = []
        for aidoo in self.aidoos.values():
            modes = aidoo.get_modes() or []
            for mode in modes:
                if mode not in mode_values:
                    mode_values += [mode]
        for zone in self.zones.values():
            modes = zone.get_modes() or []
            for mode in modes:
                if mode not in mode_values:
                    mode_values += [mode]
        if len(mode_values) > 0:
            return mode_values
        return None

    def get_name(self) -> str:
        """Return DeviceGroup name."""
        return self.name

    def get_power(self) -> bool | None:
        """Return DeviceGroup power status."""
        power_values: list[bool] = []
        for aidoo in self.aidoos.values():
            power = aidoo.get_power()
            if power is not None:
                power_values += [power]
        for zone in self.zones.values():
            power = zone.get_power()
            if power is not None:
                power_values += [power]
        if len(power_values) > 0:
            if True in power_values:
                return True
            if False in power_values:
                return False
        return None

    def get_temperature(self) -> float | None:
        """Return DeviceGroup temperature."""
        temp_values: list[float] = []
        for aidoo in self.aidoos.values():
            temp = aidoo.get_temperature()
            if temp is not None:
                temp_values += [temp]
        for zone in self.zones.values():
            temp = zone.get_temperature()
            if temp is not None:
                temp_values += [temp]
        if len(temp_values) > 0:
            temp = sum(temp_values) / len(temp_values)
            return round(temp, 1)
        return None

    def get_temp_set(self) -> float | None:
        """Return DeviceGroup setpoint."""
        temp_set_values: list[float] = []
        for aidoo in self.aidoos.values():
            temp_set = aidoo.get_temp_set()
            if temp_set is not None:
                temp_set_values += [temp_set]
        for zone in self.zones.values():
            temp_set = zone.get_temp_set()
            if temp_set is not None:
                temp_set_values += [temp_set]
        if len(temp_set_values) > 0:
            temp_set = sum(temp_set_values) / len(temp_set_values)
            return round(temp_set, 1)
        return None

    def get_temp_set_max(self) -> float | None:
        """Return DeviceGroup max setpoint."""
        temp_set_max_values: list[float] = []
        for aidoo in self.aidoos.values():
            temp_set_max = aidoo.get_temp_set_max()
            if temp_set_max is not None:
                temp_set_max_values += [temp_set_max]
        for zone in self.zones.values():
            temp_set_max = zone.get_temp_set_max()
            if temp_set_max is not None:
                temp_set_max_values += [temp_set_max]
        if len(temp_set_max_values) > 0:
            temp_set_max = sum(temp_set_max_values) / len(temp_set_max_values)
            return round(temp_set_max, 1)
        return None

    def get_temp_set_min(self) -> float | None:
        """Return DeviceGroup min setpoint."""
        temp_set_min_values: list[float] = []
        for aidoo in self.aidoos.values():
            temp_set_min = aidoo.get_temp_set_min()
            if temp_set_min is not None:
                temp_set_min_values += [temp_set_min]
        for zone in self.zones.values():
            temp_set_min = zone.get_temp_set_min()
            if temp_set_min is not None:
                temp_set_min_values += [temp_set_min]
        if len(temp_set_min_values) > 0:
            temp_set_min = sum(temp_set_min_values) / len(temp_set_min_values)
            return round(temp_set_min, 1)
        return None

    def get_temp_step(self) -> float | None:
        """Return DeviceGroup temperature step."""
        return API_DEFAULT_TEMP_STEP

    def set_params(self, params: dict[str, Any]) -> None:
        """Update DeviceGroup parameters from API request."""

        _params: dict[str, Any] = params[API_PARAMS]
        for param, value in _params.items():
            data: dict[str, Any] = {
                API_VALUE: value,
            }
            for aidoo in self.aidoos.values():
                aidoo.set_param(param, data)
            for zone in self.zones.values():
                zone.set_param(param, data)
