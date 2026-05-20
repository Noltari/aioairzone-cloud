"""Airzone Cloud API Air Quality."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .common import parse_bool, parse_float, parse_int, parse_str
from .const import (
    API_AQ_CO2,
    API_AQ_PRESSURE,
    API_AQ_QUALITY,
    API_AQ_SCORE,
    API_AQ_SENSOR_FW,
    API_AQ_TEMP,
    API_AQ_TVOC,
    API_AQ_VENT_ACTIVE,
    API_CELSIUS,
    API_HUMIDITY,
    API_NAME,
    API_SYSTEM_NUMBER,
    API_ZONE_NUMBER,
    AZD_AQ_CO2,
    AZD_AQ_PRESSURE,
    AZD_AQ_SCORE,
    AZD_AQ_STATUS,
    AZD_AQ_TEMP,
    AZD_AQ_TVOC,
    AZD_AQ_VENT_ACTIVE,
    AZD_FIRMWARE,
    AZD_HUMIDITY,
    AZD_SYSTEM,
    AZD_ZONE,
)
from .device import Device
from .entity import EntityUpdate

if TYPE_CHECKING:
    from .system import System
    from .zone import Zone

_LOGGER = logging.getLogger(__name__)


class AirQuality(Device):
    """Airzone Cloud Air Quality device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Air Quality device init."""
        super().__init__(inst_id, ws_id, device_data)

        self.aq_co2: int | None = None
        self.aq_pressure: float | None = None
        self.aq_score: int | None = None
        self.aq_sensor_fw: str | None = None
        self.aq_temp: float | None = None
        self.aq_tvoc: int | None = None
        self.aq_vent_active: bool | None = None
        self.humidity: int | None = None
        self.systems: dict[str, System] = {}
        self.zones: dict[str, Zone] = {}

        sub_data = self.sub_data(device_data)
        self.system_number = int(sub_data[API_SYSTEM_NUMBER])
        self.zone_number = int(sub_data[API_ZONE_NUMBER])

        device_name = parse_str(device_data.get(API_NAME))
        if device_name is not None:
            self.name = device_name
        else:
            self.name = f"Air Quality {self.system_number}:{self.zone_number}"

    def data(self) -> dict[str, Any]:
        """Return Air Quality device data."""
        data = super().data()

        data[AZD_SYSTEM] = self.get_system_num()
        data[AZD_ZONE] = self.get_zone_num()

        aq_co2 = self.get_aq_co2()
        if aq_co2 is not None:
            data[AZD_AQ_CO2] = aq_co2

        aq_pressure = self.get_aq_pressure()
        if aq_pressure is not None:
            data[AZD_AQ_PRESSURE] = aq_pressure

        aq_score = self.get_aq_score()
        if aq_score is not None:
            data[AZD_AQ_SCORE] = aq_score

        aq_sensor_fw = self.get_aq_sensor_fw()
        if aq_sensor_fw is not None:
            data[AZD_FIRMWARE] = aq_sensor_fw

        aq_status = self.get_aq_status()
        if aq_status is not None:
            data[AZD_AQ_STATUS] = aq_status

        aq_temp = self.get_aq_temp()
        if aq_temp is not None:
            data[AZD_AQ_TEMP] = aq_temp

        aq_tvoc = self.get_aq_tvoc()
        if aq_tvoc is not None:
            data[AZD_AQ_TVOC] = aq_tvoc

        aq_vent_active = self.get_aq_vent_active()
        if aq_vent_active is not None:
            data[AZD_AQ_VENT_ACTIVE] = aq_vent_active

        humidity = self.get_humidity()
        if humidity is not None:
            data[AZD_HUMIDITY] = humidity

        return data

    def add_system(self, system: System) -> None:
        """Add Air Quality system."""
        system_id = system.get_id()
        if system_id not in self.systems:
            self.systems[system_id] = system

    def add_zone(self, zone: Zone) -> None:
        """Add Air Quality zone."""
        zone_id = zone.get_id()
        if zone_id not in self.zones:
            self.zones[zone_id] = zone

    def get_aq_co2(self) -> int | None:
        """Return Air Quality CO2 level (ppm)."""
        return self.aq_co2

    def get_aq_pressure(self) -> float | None:
        """Return Air Quality atmospheric pressure (hPa)."""
        return self.aq_pressure

    def get_aq_score(self) -> int | None:
        """Return Air Quality overall score."""
        return self.aq_score

    def get_aq_sensor_fw(self) -> str | None:
        """Return Air Quality sensor firmware version."""
        return self.aq_sensor_fw

    def get_aq_temp(self) -> float | None:
        """Return Air Quality sensor temperature (°C)."""
        return self.aq_temp

    def get_aq_tvoc(self) -> int | None:
        """Return Air Quality TVOC level (ppb)."""
        return self.aq_tvoc

    def get_aq_vent_active(self) -> bool | None:
        """Return Air Quality ventilation active status."""
        return self.aq_vent_active

    def get_humidity(self) -> int | None:
        """Return Air Quality sensor humidity (%)."""
        return self.humidity

    def get_system_num(self) -> int:
        """Return System number."""
        return self.system_number

    def get_zone_num(self) -> int:
        """Return Zone number."""
        return self.zone_number

    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update Air Quality parameter from API request."""

    def update_data(self, update: EntityUpdate) -> None:
        """Update Air Quality data."""
        super().update_data(update)

        data = update.get_data()

        aq_co2 = parse_int(data.get(API_AQ_CO2))
        if aq_co2 is not None:
            self.aq_co2 = aq_co2

        aq_pressure = parse_float(data.get(API_AQ_PRESSURE))
        if aq_pressure is not None:
            self.aq_pressure = aq_pressure

        aq_score = parse_int(data.get(API_AQ_SCORE))
        if aq_score is not None:
            self.aq_score = aq_score

        aq_sensor_fw = parse_str(data.get(API_AQ_SENSOR_FW))
        if aq_sensor_fw is not None:
            self.aq_sensor_fw = aq_sensor_fw

        aq_status = parse_str(data.get(API_AQ_QUALITY))
        if aq_status is not None:
            self.aq_status = aq_status

        aq_temp_data = data.get(API_AQ_TEMP)
        if isinstance(aq_temp_data, dict):
            aq_temp = parse_float(aq_temp_data.get(API_CELSIUS))
            if aq_temp is not None:
                self.aq_temp = aq_temp

        aq_tvoc = parse_int(data.get(API_AQ_TVOC))
        if aq_tvoc is not None:
            self.aq_tvoc = aq_tvoc

        aq_vent_active = parse_bool(data.get(API_AQ_VENT_ACTIVE))
        if aq_vent_active is not None:
            self.aq_vent_active = aq_vent_active

        humidity = parse_int(data.get(API_HUMIDITY))
        if humidity is not None:
            self.humidity = humidity
