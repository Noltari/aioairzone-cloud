"""Airzone Cloud API Installation."""

from __future__ import annotations

from typing import Any

from .common import UserAccessType
from .const import (
    API_ACCESS_TYPE,
    API_INSTALLATION_ID,
    API_NAME,
    API_TYPE_ALL,
    API_TYPE_USER,
    API_WS_IDS,
    AZD_GROUPS,
    AZD_NUM_GROUPS,
    AZD_USER_ACCESS,
    AZD_WEBSERVERS,
)
from .device_group import DeviceGroup
from .group import Group


class Installation(DeviceGroup):
    """Airzone Cloud Installation."""

    def __init__(self, inst_data: dict[str, Any]) -> None:
        """Airzone Cloud Installation init."""
        super().__init__()

        self.groups: dict[str, Group] = {}
        self.id = str(inst_data[API_INSTALLATION_ID])
        self.user_access: UserAccessType = UserAccessType.UNKNOWN
        self.webservers: list[str] = []

        name: str = inst_data.get(API_NAME, "")
        if len(name) > 0:
            self.name = name
        else:
            self.name = "Installation"

        access_type = inst_data.get(API_ACCESS_TYPE)
        if access_type is not None:
            self.user_access = UserAccessType(str(access_type))

        for ws_id in inst_data[API_WS_IDS]:
            self.webservers += [ws_id]

    def data(self) -> dict[str, Any]:
        """Return Installation data."""
        data = super().data()

        if len(self.groups) > 0:
            data[AZD_GROUPS] = list(self.groups)

        data[AZD_NUM_GROUPS] = self.get_groups_num()
        data[AZD_USER_ACCESS] = self.get_user_access()
        data[AZD_WEBSERVERS] = self.get_webservers()

        return data

    def add_group(self, group: Group) -> None:
        """Add Group to Installation."""
        group_id = group.get_id()
        if group_id not in self.groups:
            self.groups[group_id] = group

    def get_groups_num(self) -> int:
        """Return Groups count."""
        return len(self.groups)

    def get_id(self) -> str:
        """Return Installation ID."""
        return self.id

    def get_name(self) -> str:
        """Return Installation name."""
        return self.name

    def get_request_type(self) -> str:
        """Return request type."""
        if self.user_access.is_admin():
            return API_TYPE_ALL
        return API_TYPE_USER

    def get_user_access(self) -> str:
        """Return Installation user access."""
        return self.user_access

    def get_webservers(self) -> list[str]:
        """Return Installation WebServers."""
        return self.webservers
