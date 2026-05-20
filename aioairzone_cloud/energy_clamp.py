"""Airzone Cloud API Energy Clamp."""

from __future__ import annotations

import logging
from typing import Any

from .common import parse_float, parse_str
from .const import (
    API_CURRENT_TOTAL,
    API_ENERGY_ACC,
    API_ENERGY_PERIOD_END_DT,
    API_ENERGY_RET,
    API_NAME,
    API_POWER_TOTAL,
    API_SYSTEM_NUMBER,
    API_VOLTAGE_TOTAL,
    API_ZONE_NUMBER,
    AZD_CURRENT,
    AZD_ENERGY_ACC,
    AZD_ENERGY_PERIOD_END,
    AZD_ENERGY_RET,
    AZD_POWER_TOTAL,
    AZD_SYSTEM,
    AZD_VOLTAGE,
    AZD_ZONE,
)
from .device import Device
from .entity import EntityUpdate

_LOGGER = logging.getLogger(__name__)


class EnergyClamp(Device):
    """Airzone Cloud Energy Clamp device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Energy Clamp device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.current_total: float | None = None
        self.energy_acc: float | None = None
        self.energy_period_end: str | None = None
        self.energy_ret: float | None = None
        self.power_total: float | None = None
        self.voltage_total: float | None = None

        sub_data = self.sub_data(device_data)
        self.system_number = int(sub_data[API_SYSTEM_NUMBER])
        self.zone_number = int(sub_data[API_ZONE_NUMBER])

        device_name = parse_str(device_data.get(API_NAME))
        if device_name is not None:
            self.name = device_name
        else:
            self.name = f"Energy Clamp {self.system_number}:{self.zone_number}"

    def data(self) -> dict[str, Any]:
        """Return Energy Clamp device data."""
        data = super().data()

        data[AZD_SYSTEM] = self.get_system_num()
        data[AZD_ZONE] = self.get_zone_num()

        current_total = self.get_current_total()
        if current_total is not None:
            data[AZD_CURRENT] = current_total

        energy_acc = self.get_energy_acc()
        if energy_acc is not None:
            data[AZD_ENERGY_ACC] = energy_acc

        energy_period_end = self.get_energy_period_end()
        if energy_period_end is not None:
            data[AZD_ENERGY_PERIOD_END] = energy_period_end

        energy_ret = self.get_energy_ret()
        if energy_ret is not None:
            data[AZD_ENERGY_RET] = energy_ret

        power_total = self.get_power_total()
        if power_total is not None:
            data[AZD_POWER_TOTAL] = power_total

        voltage_total = self.get_voltage_total()
        if voltage_total is not None:
            data[AZD_VOLTAGE] = voltage_total

        return data

    def get_current_total(self) -> float | None:
        """Return measured current (A)."""
        return self.current_total

    def get_energy_acc(self) -> float | None:
        """Return accumulated energy consumption (kWh)."""
        return self.energy_acc

    def get_energy_period_end(self) -> str | None:
        """Return energy measurement period end timestamp."""
        return self.energy_period_end

    def get_energy_ret(self) -> float | None:
        """Return returned/exported energy (kWh)."""
        return self.energy_ret

    def get_power_total(self) -> float | None:
        """Return current power consumption (W)."""
        return self.power_total

    def get_system_num(self) -> int:
        """Return system number."""
        return self.system_number

    def get_voltage_total(self) -> float | None:
        """Return measured voltage (V)."""
        return self.voltage_total

    def get_zone_num(self) -> int:
        """Return zone number."""
        return self.zone_number

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update Energy Clamp parameter from API request."""

    def update_data(self, update: EntityUpdate) -> None:
        """Update Energy Clamp data."""
        super().update_data(update)

        data = update.get_data()

        current_total = parse_float(data.get(API_CURRENT_TOTAL))
        if current_total is not None:
            self.current_total = current_total

        energy_acc = parse_float(data.get(API_ENERGY_ACC))
        if energy_acc is not None:
            self.energy_acc = energy_acc

        energy_period_end = parse_str(data.get(API_ENERGY_PERIOD_END_DT))
        if energy_period_end is not None:
            self.energy_period_end = energy_period_end

        energy_ret = parse_float(data.get(API_ENERGY_RET))
        if energy_ret is not None:
            self.energy_ret = energy_ret

        power_total = parse_float(data.get(API_POWER_TOTAL))
        if power_total is not None:
            self.power_total = power_total

        voltage_total = parse_float(data.get(API_VOLTAGE_TOTAL))
        if voltage_total is not None:
            self.voltage_total = voltage_total
