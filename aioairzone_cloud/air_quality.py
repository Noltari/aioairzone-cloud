"""Airzone Cloud API Air Quality."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any


from .common import parse_bool, parse_int, parse_str, parse_float
from .const import (
    API_AQ_PM_1,
    API_AQ_PM_2P5,
    API_AQ_PM_10,
    API_AQ_CO2,
    API_AQ_TVOC,
    API_AQ_HUMIDITY,
    API_AQ_TEMP,
    API_AQ_TEMP_CELSIUS,
    API_AQ_PRESSURE,
    API_AQ_PRESENT,
    API_AQ_VENT_ACTIVE,
    API_AQ_QUALITY,
    API_AQ_QUALITY_LEVELS,
    API_AQ_SCORE,
    API_AQ_SENSOR_FW,
    API_NAME,
    API_SYSTEM_NUMBER,
    API_ZONE_NUMBER,
    AZD_AQ_VENT_ACTIVE,
    AZD_AQ_QUALITY,
    AZD_AQ_SCORE,
    AZD_AQ_PM_1,
    AZD_AQ_PM_2P5,
    AZD_AQ_PM_10,
    AZD_AQ_CO2,
    AZD_AQ_TVOC,
    AZD_AQ_HUMIDITY,
    AZD_AQ_TEMP,
    AZD_AQ_PRESSURE,
    AZD_AQ_PRESENT,
    AZD_AQ_QUALITY,
    AZD_FIRMWARE,
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

        self.aq_sensor_fw: str | None = None
        self.systems: dict[str, System] = {}
        self.zones: dict[str, Zone] = {}

        self.aq_vent_active: bool | None = None
        self.aq_pm_1: int | None = None
        self.aq_pm_2p5: int | None = None
        self.aq_pm_10: int | None = None
        self.aq_co2: int | None = None
        self.aq_tvoc: int | None = None
        self.aq_humidity: int | None = None
        self.aq_temp: float | None = None
        self.aq_pressure: float | None = None
        self.aq_present: bool | None = None
        self.aq_quality: str | None = None
        self.aq_score: int | None = None

        sub_data = self.sub_data(device_data)
        self.system_number = int(sub_data[API_SYSTEM_NUMBER])
        self.zone_number = int(sub_data[API_ZONE_NUMBER])

        device_name = parse_str(device_data.get(API_NAME))
        if device_name is not None:
            self.name = device_name
        else:
            self.name = f"Air Quality {self.system_number}:{self.zone_number}"

    def data(self) -> dict[str, Any]:
        """Return System device data."""
        data = super().data()

        aq_vent_active = self.get_aq_vent_active()
        if aq_vent_active is not None:
            data[AZD_AQ_VENT_ACTIVE] = aq_vent_active

        aq_quality = self.get_aq_quality()
        if aq_quality is not None:
            for key, value in API_AQ_QUALITY_LEVELS.items():
                if aq_quality == key:
                    data[AZD_AQ_QUALITY] = value

        aq_score = self.get_aq_score()
        if aq_score is not None:
            data[AZD_AQ_SCORE] = aq_score

        aq_pm_1 = self.get_aq_pm_1()
        if aq_pm_1 is not None:
            data[AZD_AQ_PM_1] = aq_pm_1

        aq_pm_2p5 = self.get_aq_pm_2p5()
        if aq_pm_2p5 is not None:
            data[AZD_AQ_PM_2P5] = aq_pm_2p5

        aq_pm_10 = self.get_aq_pm_10()
        if aq_pm_10 is not None:
            data[AZD_AQ_PM_10] = aq_pm_10

        aq_co2 = self.get_aq_co2()
        if aq_co2 is not None:
            data[AZD_AQ_CO2] = aq_co2

        aq_tvoc = self.get_aq_tvoc()
        if aq_tvoc is not None:
            data[AZD_AQ_TVOC] = aq_tvoc

        aq_humidity = self.get_aq_humidity()
        if aq_humidity is not None:
            data[AZD_AQ_HUMIDITY] = aq_humidity

        aq_temp = self.get_aq_temp()
        if aq_temp is not None:
            data[AZD_AQ_TEMP] = aq_temp

        aq_pressure = self.get_aq_pressure()
        if aq_pressure is not None:
            data[AZD_AQ_PRESSURE] = aq_pressure

        aq_present = self.get_aq_present()
        if aq_present is not None:
            data[AZD_AQ_PRESENT] = aq_present

        data[AZD_SYSTEM] = self.get_system_num()
        data[AZD_ZONE] = self.get_zone_num()

        aq_sensor_fw = self.get_aq_sensor_fw()
        if aq_sensor_fw is not None:
            data[AZD_FIRMWARE] = aq_sensor_fw

        return data

    def get_aq_vent_active(self) -> bool | None:
        """Return HVAC device Air Quality ventilation active status."""
        if self.air_quality is not None:
            return self.air_quality.aq_vent_active
        return self.aq_vent_active

    def get_aq_quality(self) -> str | None:
        """Return HVAC device Air Quality quality."""
        if self.air_quality is not None:
            return self.air_quality.aq_quality
        return self.aq_quality

    def get_aq_score(self) -> int | None:
        """Return HVAC device Air Quality SCORE."""
        if self.air_quality is not None:
            return self.air_quality.aq_score
        return self.aq_score

    def get_aq_pm_1(self) -> int | None:
        """Return HVAC device Air Quality PM 1."""
        if self.air_quality is not None:
            return self.air_quality.aq_pm_1
        return self.aq_pm_1

    def get_aq_pm_2p5(self) -> int | None:
        """Return HVAC device Air Quality PM 2.5."""
        if self.air_quality is not None:
            return self.air_quality.aq_pm_2p5
        return self.aq_pm_2p5

    def get_aq_pm_10(self) -> int | None:
        """Return HVAC device Air Quality PM 10."""
        if self.air_quality is not None:
            return self.air_quality.aq_pm_10
        return self.aq_pm_10

    def get_aq_co2(self) -> int | None:
        """Return HVAC device Air Quality CO2."""
        if self.air_quality is not None:
            return self.air_quality.aq_co2
        return self.aq_co2

    def get_aq_tvoc(self) -> int | None:
        """Return HVAC device Air Quality TVOC."""
        if self.air_quality is not None:
            return self.air_quality.aq_tvoc
        return self.aq_tvoc

    def get_aq_temp(self) -> int | None:
        """Return HVAC device Air Quality Temperature."""
        if self.air_quality is not None:
            return self.air_quality.aq_temp
        return self.aq_temp

    def get_aq_pressure(self) -> int | None:
        """Return HVAC device Air Quality Pressure."""
        if self.air_quality is not None:
            return self.air_quality.aq_pressure
        return self.aq_pressure

    def get_aq_humidity(self) -> int | None:
        """Return HVAC device Air Quality Humidity."""
        if self.air_quality is not None:
            return self.air_quality.aq_humidity
        return self.aq_humidity

    def get_aq_present(self) -> bool | None:
        """Return HVAC device Air Quality present."""
        if self.air_quality is not None:
            return self.air_quality.aq_present
        return self.aq_present

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

    def get_aq_sensor_fw(self) -> str | None:
        """Return Zone Air Quality sensor FW."""
        return self.aq_sensor_fw

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

        aq_vent_active = parse_bool(data.get(API_AQ_VENT_ACTIVE))
        if aq_vent_active is not None:
            self.aq_vent_active = aq_vent_active

        aq_pm_1 = parse_int(data.get(API_AQ_PM_1))
        if aq_pm_1 is not None:
            self.aq_pm_1 = aq_pm_1

        aq_pm_2p5 = parse_int(data.get(API_AQ_PM_2P5))
        if aq_pm_2p5 is not None:
            self.aq_pm_2p5 = aq_pm_2p5

        aq_pm_10 = parse_int(data.get(API_AQ_PM_10))
        if aq_pm_10 is not None:
            self.aq_pm_10 = aq_pm_10

        aq_co2 = parse_int(data.get(API_AQ_CO2))
        if aq_co2 is not None:
            self.aq_co2 = aq_co2

        aq_tvoc = parse_int(data.get(API_AQ_TVOC))
        if aq_tvoc is not None:
            self.aq_tvoc = aq_tvoc

        aq_humidity = parse_int(data.get(API_AQ_HUMIDITY))
        if aq_humidity is not None:
            self.aq_humidity = aq_humidity

        aq_temp = data.get(API_AQ_TEMP)
        if aq_temp is not None:
            aq_temp = parse_float(aq_temp.get(API_AQ_TEMP_CELSIUS))
            self.aq_temp = aq_temp

        aq_pressure = data.get(API_AQ_PRESSURE)
        if aq_pressure is not None:
            self.aq_pressure = aq_pressure

        aq_present = parse_bool(data.get(API_AQ_PRESENT))
        if aq_present is not None:
            self.aq_present = aq_present

        aq_quality = parse_str(data.get(API_AQ_QUALITY))
        if aq_quality is not None:
            self.aq_quality = aq_quality

        aq_score = parse_str(data.get(API_AQ_SCORE))
        if aq_score is not None:
            self.aq_score = aq_score

        aq_sensor_fw = parse_str(data.get(API_AQ_SENSOR_FW))
        if aq_sensor_fw is not None:
            self.aq_sensor_fw = aq_sensor_fw
