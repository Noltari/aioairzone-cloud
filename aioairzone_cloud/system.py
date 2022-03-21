"""Airzone Cloud API System."""
from __future__ import annotations

from typing import Any

from .device import Device


class System(Device):
    """Airzone Cloud System."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud System init."""
        super().__init__(inst_id, ws_id, device_data)

        self.name = f"System {self.get_system()}"
