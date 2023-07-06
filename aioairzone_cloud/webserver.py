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
    API_STAT_RSSI,
    API_STAT_SSID,
    API_STATUS,
    API_WS_FW,
    API_WS_TYPE,
    AZD_AVAILABLE,
    AZD_CONNECTION_DATE,
    AZD_DISCONNECTION_DATE,
    AZD_FIRMWARE,
    AZD_ID,
    AZD_INSTALLATION,
    AZD_NAME,
    AZD_TYPE,
    AZD_WIFI_CHANNEL,
    AZD_WIFI_MAC,
    AZD_WIFI_QUALITY,
    AZD_WIFI_RSSI,
    AZD_WIFI_SSID,
)


class WebServer:
    """Airzone Cloud WebServer."""

    def __init__(self, inst_id: str, ws_id: str):
        """Airzone Cloud WebServer init."""
        self.connection_date: str | None = None
        self.disconnection_date: str | None = None
        self.firmware: str | None = None
        self.id = ws_id
        self.installation_id = inst_id
        self.is_connected: bool = False
        self.name: str = f"WebServer {ws_id}"
        self.stat_quality: int | None = None
        self.type: str | None = None
        self.wifi_channel: int | None = None
        self.wifi_mac: str | None = None
        self.wifi_quality: int | None = None
        self.wifi_rssi: int | None = None
        self.wifi_ssid: str | None = None

    def update(self, data: dict[str, Any]) -> None:
        """Update WebServer data."""

        ws_type = data.get(API_WS_TYPE)
        if ws_type is not None:
            self.type = str(ws_type)

        ws_config = data.get(API_CONFIG)
        if ws_config is not None:
            stat_ap_mac = ws_config.get(API_STAT_AP_MAC)
            if stat_ap_mac is not None:
                self.wifi_mac = str(stat_ap_mac)
            stat_channel = ws_config.get(API_STAT_CHANNEL)
            if stat_channel is not None:
                self.wifi_channel = int(stat_channel)
            stat_ssid = ws_config.get(API_STAT_SSID)
            if stat_ssid is not None:
                self.wifi_ssid = str(stat_ssid)
            ws_fw = ws_config.get(API_WS_FW)
            if ws_fw is not None:
                self.firmware = str(ws_fw)

        ws_status = data.get(API_STATUS)
        if ws_status is not None:
            connection_date = ws_status.get(API_CONNECTION_DATE)
            if connection_date is not None:
                self.connection_date = str(connection_date)
            disconnection_date = ws_status.get(API_DISCONNECTION_DATE)
            if disconnection_date is not None:
                self.disconnection_date = str(disconnection_date)
            is_connected = ws_status.get(API_IS_CONNECTED)
            if is_connected is not None:
                self.is_connected = bool(is_connected)
            stat_quality = ws_status.get(API_STAT_QUALITY)
            if stat_quality is not None:
                self.wifi_quality = int(stat_quality)
            stat_rssi = ws_status.get(API_STAT_RSSI)
            if stat_rssi is not None:
                self.wifi_rssi = int(stat_rssi)

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
