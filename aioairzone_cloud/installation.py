"""Airzone Cloud API Installation."""
from __future__ import annotations

from typing import Any

from .const import (
    API_INSTALLATION_ID,
    API_NAME,
    API_WS_IDS,
    AZD_ID,
    AZD_NAME,
    AZD_WEBSERVERS,
)


class Installation:
    """Airzone Cloud Installation."""

    def __init__(self, inst_data):
        """Airzone Cloud Installation init."""
        self.id = str(inst_data[API_INSTALLATION_ID])
        self.name = str(inst_data[API_NAME])
        self.webservers: list[str] = []

        for ws_id in inst_data[API_WS_IDS]:
            self.webservers.append(ws_id)

    def data(self) -> dict[str, Any]:
        """Return Installation data."""
        data: dict[str, Any] = {
            AZD_ID: self.get_id(),
            AZD_NAME: self.get_name(),
            AZD_WEBSERVERS: self.get_webservers(),
        }

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
