"""Airzone Cloud API common code."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Any


@dataclass
class ConnectionOptions:
    """Airzone Cloud options for connection."""

    username: str
    password: str
    websockets: bool = True


class AirQualityMode(StrEnum):
    """Airzone Cloud air quality modes."""

    UNKNOWN = "unknown"

    OFF = "off"
    ON = "on"
    AUTO = "auto"

    @classmethod
    def _missing_(cls, value: Any) -> AirQualityMode:
        return cls.UNKNOWN


class OperationAction(IntEnum):
    """Airzone Cloud operation actions."""

    COOLING = 1
    DRYING = 2
    FAN = 3
    HEATING = 4
    IDLE = 5
    OFF = 6


class OperationMode(IntEnum):
    """Airzone Cloud operation modes."""

    STOP = 0
    AUTO = 1
    COOLING = 2
    HEATING = 3
    VENTILATION = 4
    DRY = 5
    EMERGENCY_HEAT = 6
    HEAT_AIR = 7
    HEAT_RADIANT = 8
    HEAT_COMBINED = 9
    COOLING_AIR = 10
    COOLING_RADIANT = 11
    COOLING_COMBINED = 12

    def is_auto(self) -> bool:
        """Return if mode is Auto."""
        return self.value in [self.AUTO]

    def is_cool(self) -> bool:
        """Return if mode is Cool."""
        return self.value in [
            self.COOLING,
            self.COOLING_AIR,
            self.COOLING_COMBINED,
            self.COOLING_RADIANT,
        ]

    def is_dry(self) -> bool:
        """Return if mode is Dry."""
        return self.value in [self.DRY]

    def is_heat(self) -> bool:
        """Return if mode is Heat."""
        return self.value in [
            self.EMERGENCY_HEAT,
            self.HEATING,
            self.HEAT_AIR,
            self.HEAT_COMBINED,
            self.HEAT_RADIANT,
        ]

    def is_stop(self) -> bool:
        """Return if mode is Stop."""
        return self.value in [self.STOP]

    def is_vent(self) -> bool:
        """Return if mode is Ventilation."""
        return self.value in [self.VENTILATION]


class SpeedType(IntEnum):
    """Airzone Cloud speed type."""

    NORMAL = 0
    AIRFLOW = 1


class TemperatureUnit(IntEnum):
    """Airzone Cloud temperature units."""

    CELSIUS = 0
    FAHRENHEIT = 1
