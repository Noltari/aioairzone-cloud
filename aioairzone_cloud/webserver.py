"""Airzone Cloud Local API based device."""
from __future__ import annotations

from typing import Any

from .const import (
    API_CONFIG,
    API_CONNECTION_DATE,
    API_DISCONNECTION_DATE,
    API_IS_CONNECTED,
    API_STAT_AP_MAC,
    API_STAT_CHANNEL,
    API_STAT_QUALITY,
    API_STAT_SSID,
    API_STATUS,
    API_WS_FW,
    API_WS_TYPE,
    AZD_CONNECTED,
    AZD_CONNECTION_DATE,
    AZD_DISCONNECTION_DATE,
    AZD_FIRMWARE,
    AZD_ID,
    AZD_INSTALLATION,
    AZD_TYPE,
    AZD_WIFI_CHANNEL,
    AZD_WIFI_MAC,
    AZD_WIFI_QUALITY,
    AZD_WIFI_SSID,
)


class WebServer:
    """Airzone Cloud WebServer."""

    def __init__(self, inst_id: str, ws_id: str):
        """Airzone Cloud WebServer init."""
        self.connected: bool | None = None
        self.connection_date: str | None = None
        self.disconnection_date: str | None = None
        self.firmware: str | None = None
        self.id = ws_id
        self.installation_id = inst_id
        self.stat_quality: int | None = None
        self.type: str | None = None
        self.wifi_channel: int | None = None
        self.wifi_mac: str | None = None
        self.wifi_quality: int | None = None
        self.wifi_ssid: str | None = None

    def update(self, data) -> None:
        """Update WebServer data."""
        self.connected = bool(data[API_STATUS][API_IS_CONNECTED])
        self.connection_date = str(data[API_STATUS][API_CONNECTION_DATE])
        self.disconnection_date = str(data[API_STATUS][API_DISCONNECTION_DATE])
        self.firmware = str(data[API_CONFIG][API_WS_FW])
        self.type = str(data[API_WS_TYPE])
        self.wifi_channel = int(data[API_CONFIG][API_STAT_CHANNEL])
        self.wifi_mac = str(data[API_CONFIG][API_STAT_AP_MAC])
        self.wifi_quality = int(data[API_STATUS][API_STAT_QUALITY])
        self.wifi_ssid = str(data[API_CONFIG][API_STAT_SSID])

    def data(self) -> dict[str, Any]:
        """Return WebServer data."""
        return {
            AZD_CONNECTED: self.get_connected(),
            AZD_CONNECTION_DATE: self.get_connection_date(),
            AZD_DISCONNECTION_DATE: self.get_disconnection_date(),
            AZD_FIRMWARE: self.get_firmware(),
            AZD_ID: self.get_id(),
            AZD_INSTALLATION: self.get_installation(),
            AZD_TYPE: self.get_type(),
            AZD_WIFI_CHANNEL: self.get_wifi_channel(),
            AZD_WIFI_MAC: self.get_wifi_mac(),
            AZD_WIFI_QUALITY: self.get_wifi_quality(),
            AZD_WIFI_SSID: self.get_wifi_ssid(),
        }

    def get_connected(self) -> bool | None:
        """Return connected status."""
        return self.connected

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

    def get_wifi_ssid(self) -> str | None:
        """Return WiFi SSID."""
        return self.wifi_ssid
