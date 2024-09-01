"""Airzone Cloud API Device."""

from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import Lock
from datetime import datetime
from enum import IntEnum
import logging
from typing import Any

from .const import WS_ADV_CONF, WS_CHANGE, WS_STATUS

_LOGGER = logging.getLogger(__name__)


class UpdateType(IntEnum):
    """Airzone Cloud Update type."""

    API_FULL = 1
    WS_FULL = 2
    WS_PARTIAL = 3


class EntityUpdate:
    """Airzone Cloud Entity Update."""

    data: dict[str, Any]

    def __init__(self, _type: UpdateType, data: dict[str, Any]):
        """Airzone Cloud Update init."""
        self.datetime: datetime = datetime.now()
        self.data: dict[str, Any] = data
        self.type: UpdateType = _type

    def check_dt(self, dt: datetime) -> bool:
        """Check if Update data is newer than provided datetime."""
        return self.datetime >= dt

    def get_data(self) -> dict[str, Any]:
        """Get Entity Update data."""
        if self.type == UpdateType.WS_PARTIAL:
            change: dict[str, Any] = self.data.get(WS_CHANGE, {})
            adv_conf: dict[str, Any] = change.get(WS_ADV_CONF, {})
            status: dict[str, Any] = change.get(WS_STATUS, {})
            return adv_conf | status

        return self.data

    def get_datetime(self) -> datetime:
        """Get Entity Update datetime."""
        return self.datetime

    def get_type(self) -> UpdateType:
        """Get Entity Update type."""
        return self.type

    def set_data(self, data: dict[str, Any]) -> None:
        """Set Entity Update data."""
        self.data = data

    def __str__(self) -> str:
        """Return Entity Update string representation."""
        _data = self.get_data()
        _type = self.get_type()
        return f"{_type} with data={_data}"


class Entity(ABC):
    """Airzone Cloud Entity."""

    datetime: datetime
    id: str
    lock: Lock
    name: str

    def __init__(self) -> None:
        """Airzone Cloud Device init."""
        self.datetime: datetime = datetime.now()
        self.init: bool = False
        self.lock: Lock = Lock()

    @abstractmethod
    def data(self) -> dict[str, Any]:
        """Return Entity data."""

    def get_id(self) -> str:
        """Return Entity ID."""
        return self.id

    def get_init(self) -> bool:
        """Return Entity Init."""
        return self.init

    def get_name(self) -> str:
        """Return Entity name."""
        return self.name

    @abstractmethod
    def update_data(self, update: EntityUpdate) -> None:
        """Update Entity data."""

    async def update(self, update: EntityUpdate) -> None:
        """Update Entity."""
        newer: bool = update.check_dt(self.datetime)

        _LOGGER.debug(
            "%s[%s] update (newer=%s) update=%s",
            type(self).__name__,
            self.get_id(),
            newer,
            update,
        )

        if newer:
            async with self.lock:
                self.update_data(update)
                self.datetime = update.get_datetime()
                if update.get_type() == UpdateType.API_FULL:
                    self.init = True
