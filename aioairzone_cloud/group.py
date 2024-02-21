"""Airzone Cloud API Group."""

from __future__ import annotations

from typing import Any

from .const import API_GROUP_ID, API_NAME, AZD_INSTALLATION
from .device_group import DeviceGroup


class Group(DeviceGroup):
    """Airzone Cloud Group."""

    def __init__(self, inst_id: str, group_data: dict[str, Any]) -> None:
        """Airzone Cloud Group init."""
        super().__init__()

        self.id = str(group_data[API_GROUP_ID])
        self.installation_id = inst_id

        name: str = group_data.get(API_NAME, "")
        if len(name) > 0:
            self.name = name
        else:
            self.name = "Group"

    def data(self) -> dict[str, Any]:
        """Return Group data."""
        data = super().data()

        data[AZD_INSTALLATION] = self.get_installation()

        return data

    def get_installation(self) -> str:
        """Return Installation ID."""
        return self.installation_id
