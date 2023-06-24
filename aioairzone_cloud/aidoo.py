"""Airzone Cloud API Aidoo device."""
from __future__ import annotations

from typing import Any

from .const import API_NAME
from .hvac import HVAC


class Aidoo(HVAC):
    """Airzone Cloud Aidoo device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Aidoo device init."""
        super().__init__(inst_id, ws_id, device_data)

        if API_NAME in device_data:
            self.name = str(device_data[API_NAME])
        else:
            self.name = f"Aidoo {ws_id}"
