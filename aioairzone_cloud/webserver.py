"""Airzone Cloud Local API based device."""

from __future__ import annotations

import logging
from typing import Any

from .common import parse_bool, parse_int, parse_str
from .const import (
    API_CONFIG,
    API_CONNECTION_DATE,
    API_CPU_WS,
    API_DISCONNECTION_DATE,
    API_FREE,
    API_FREE_MEM,
    API_GENERAL,
    API_IS_CONNECTED,
    API_STAT_AP_MAC,
    API_STAT_CHANNEL,
    API_STAT_QUALITY,
    API_STAT_RSSI,
    API_STAT_SSID,
    API_STATUS,
    API_WS_FW,
    API_WS_TYPE,
    AZD_AVAILABLE,
    AZD_CONNECTION_DATE,
    AZD_CPU_USAGE,
    AZD_DISCONNECTION_DATE,
    AZD_FIRMWARE,
    AZD_ID,
    AZD_INSTALLATION,
    AZD_MEMORY_FREE,
    AZD_NAME,
    AZD_TYPE,
    AZD_WIFI_CHANNEL,
    AZD_WIFI_MAC,
    AZD_WIFI_QUALITY,
    AZD_WIFI_RSSI,
    AZD_WIFI_SSID,
)
from .entity import Entity, EntityUpdate, UpdateType

_LOGGER = logging.getLogger(__name__)


class WebServer(Entity):
    """Airzone Cloud WebServer."""

    def __init__(self, inst_id: str, ws_id: str):
        """Airzone Cloud WebServer init."""
        super().__init__()

        self.cpu_usage: int | None = None
        self.connection_date: str | None = None
        self.disconnection_date: str | None = None
        self.firmware: str | None = None
        self.id = ws_id
        self.installation_id = inst_id
        self.is_connected: bool = False
        self.memory_free: int | None = None
        self.name: str = f"WebServer {ws_id}"
        self.stat_quality: int | None = None
        self.type: str | None = None
        self.wifi_channel: int | None = None
        self.wifi_mac: str | None = None
        self.wifi_quality: int | None = None
        self.wifi_rssi: int | None = None
        self.wifi_ssid: str | None = None

    def update_data(self, update: EntityUpdate) -> None:
        """Update WebServer data."""
        data = update.get_data()

        ws_type = parse_str(data.get(API_WS_TYPE))
        if ws_type is not None:
            self.type = ws_type

        if update.get_type() != UpdateType.WS_PARTIAL:
            ws_config = data.get(API_CONFIG)
            ws_status = data.get(API_STATUS)
        else:
            ws_config = None
            ws_status = data

        if ws_config is not None:
            stat_ap_mac = parse_str(ws_config.get(API_STAT_AP_MAC))
            if stat_ap_mac is not None:
                self.wifi_mac = stat_ap_mac
            stat_channel = parse_int(ws_config.get(API_STAT_CHANNEL))
            if stat_channel is not None:
                self.wifi_channel = stat_channel
            stat_ssid = parse_str(ws_config.get(API_STAT_SSID))
            if stat_ssid is not None:
                self.wifi_ssid = stat_ssid
            ws_fw = parse_str(ws_config.get(API_WS_FW))
            if ws_fw is not None:
                self.firmware = ws_fw

        if ws_status is not None:
            connection_date = parse_str(ws_status.get(API_CONNECTION_DATE))
            if connection_date is not None:
                self.connection_date = connection_date
            cpu_usage = parse_int(ws_status.get(API_CPU_WS, {}).get(API_GENERAL))
            if cpu_usage is not None:
                self.cpu_usage = cpu_usage
            disconnection_date = parse_str(ws_status.get(API_DISCONNECTION_DATE))
            if disconnection_date is not None:
                self.disconnection_date = disconnection_date
            is_connected = parse_bool(ws_status.get(API_IS_CONNECTED))
            if is_connected is not None:
                self.is_connected = is_connected
            memory_free = parse_int(ws_status.get(API_FREE_MEM, {}).get(API_FREE))
            if memory_free is not None:
                self.memory_free = memory_free
            stat_quality = parse_int(ws_status.get(API_STAT_QUALITY))
            if stat_quality is not None:
                self.wifi_quality = stat_quality
            stat_rssi = parse_int(ws_status.get(API_STAT_RSSI))
            if stat_rssi is not None:
                self.wifi_rssi = stat_rssi

    def data(self) -> dict[str, Any]:
        """Return WebServer data."""
        data: dict[str, Any] = {
            AZD_AVAILABLE: self.get_available(),
            AZD_CONNECTION_DATE: self.get_connection_date(),
            AZD_DISCONNECTION_DATE: self.get_disconnection_date(),
            AZD_FIRMWARE: self.get_firmware(),
            AZD_ID: self.get_id(),
            AZD_INSTALLATION: self.get_installation(),
            AZD_NAME: self.get_name(),
            AZD_TYPE: self.get_type(),
        }

        cpu_usage = self.get_cpu_usage()
        if cpu_usage is not None:
            data[AZD_CPU_USAGE] = cpu_usage

        memory_free = self.get_memory_free()
        if memory_free is not None:
            data[AZD_MEMORY_FREE] = memory_free

        wifi_channel = self.get_wifi_channel()
        if wifi_channel is not None:
            data[AZD_WIFI_CHANNEL] = wifi_channel

        wifi_mac = self.get_wifi_mac()
        if wifi_mac is not None:
            data[AZD_WIFI_MAC] = wifi_mac

        wifi_quality = self.get_wifi_quality()
        if wifi_quality is not None:
            data[AZD_WIFI_QUALITY] = wifi_quality

        wifi_rssi = self.get_wifi_rssi()
        if wifi_rssi is not None:
            data[AZD_WIFI_RSSI] = wifi_rssi

        wifi_ssid = self.get_wifi_ssid()
        if wifi_ssid is not None:
            data[AZD_WIFI_SSID] = wifi_ssid

        return data

    def get_available(self) -> bool:
        """Return availability status."""
        return self.is_connected

    def get_cpu_usage(self) -> int | None:
        """Return CPU load percentage."""
        return self.cpu_usage

    def get_connection_date(self) -> str | None:
        """Return connection date."""
        return self.connection_date

    def get_disconnection_date(self) -> str | None:
        """Return disconnection date."""
        return self.disconnection_date

    def get_firmware(self) -> str | None:
        """Return firmware version."""
        return self.firmware

    def get_id(self) -> str:
        """Return WebServer ID."""
        return self.id

    def get_installation(self) -> str:
        """Return installation ID."""
        return self.installation_id

    def get_memory_free(self) -> int | None:
        """Return free memory."""
        return self.memory_free

    def get_name(self) -> str:
        """Return WebServer name."""
        return self.name

    def get_type(self) -> str | None:
        """Return WebServer type."""
        return self.type

    def get_wifi_channel(self) -> int | None:
        """Return WiFi channel."""
        return self.wifi_channel

    def get_wifi_mac(self) -> str | None:
        """Return WiFi Mac address."""
        return self.wifi_mac

    def get_wifi_quality(self) -> int | None:
        """Return WiFi signal quality."""
        return self.wifi_quality

    def get_wifi_rssi(self) -> int | None:
        """Return WiFi RSSI."""
        return self.wifi_rssi

    def get_wifi_ssid(self) -> str | None:
        """Return WiFi SSID."""
        return self.wifi_ssid
