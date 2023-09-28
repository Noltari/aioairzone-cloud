"""Airzone Cloud API Installation."""
from __future__ import annotations

from typing import Any

from .const import API_INSTALLATION_ID, API_NAME, API_WS_IDS, AZD_WEBSERVERS
from .device_group import DeviceGroup


class Installation(DeviceGroup):
    """Airzone Cloud Installation."""

    def __init__(self, inst_data: dict[str, Any]) -> None:
        """Airzone Cloud Installation init."""
        super().__init__()

        self.id = str(inst_data[API_INSTALLATION_ID])
        self.webservers: list[str] = []

        name: str = inst_data.get(API_NAME, "")
        if len(name) > 0:
            self.name = name
        else:
            self.name = "Installation"

        for ws_id in inst_data[API_WS_IDS]:
            self.webservers += [ws_id]

    def data(self) -> dict[str, Any]:
        """Return Installation data."""
        data = super().data()

        data[AZD_WEBSERVERS] = self.get_webservers()

        return data

    def get_id(self) -> str:
        """Return Installation ID."""
        return self.id

    def get_name(self) -> str:
        """Return Installation name."""
        return self.name

    def get_webservers(self) -> list[str]:
        """Return Installation WebServers."""
        return self.webservers
