"""Airzone Cloud API common code."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AirzoneStages(int, Enum):
    """Airzone stages."""

    Air = 1
    Radiant = 2
    Combined = 3


@dataclass
class ConnectionOptions:
    """Airzone Cloud options for connection."""

    username: str
    password: str


class OperationMode(int, Enum):
    """Airzone operation modes."""

    STOP = 1
    COOLING = 2
    HEATING = 3
    FAN = 4
    DRY = 5
    AUTO = 7


class TemperatureUnit(int, Enum):
    """Airzone temperature units."""

    CELSIUS = 0
    FAHRENHEIT = 1
