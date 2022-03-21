"""Airzone Cloud API."""
from __future__ import annotations

import logging
import urllib.parse
from typing import Any, cast

from aiohttp import ClientConnectorError, ClientSession
from aiohttp.client_reqrep import ClientResponse

from .common import ConnectionOptions
from .const import (
    API_AUTH_LOGIN,
    API_AUTH_REFRESH_TOKEN,
    API_AZ_SYSTEM,
    API_AZ_ZONE,
    API_CONFIG,
    API_DEVICE_ID,
    API_DEVICE_TYPE,
    API_DEVICES,
    API_EMAIL,
    API_INSTALLATION_ID,
    API_INSTALLATIONS,
    API_PASSWORD,
    API_REFRESH_TOKEN,
    API_STATUS,
    API_TOKEN,
    API_URL,
    API_USER,
    API_USER_LOGOUT,
    API_V1,
    API_WS,
    AZD_INSTALLATIONS,
    AZD_SYSTEMS,
    AZD_WEBSERVERS,
    AZD_ZONES,
    HEADER_AUTHORIZATION,
    HEADER_BEARER,
    HTTP_CALL_TIMEOUT,
)
from .device import Device
from .exceptions import LoginError, TokenRefreshError
from .installation import Installation
from .system import System
from .webserver import WebServer
from .zone import Zone

_LOGGER = logging.getLogger(__name__)


class AirzoneCloudApi:
    """Airzone Cloud API."""

    def __init__(
        self,
        aiohttp_session: ClientSession,
        options: ConnectionOptions,
    ):
        """Airzone Cloud API init."""
        self.aiohttp_session = aiohttp_session
        self.installations: list[Installation] = []
        self.options = options
        self.refresh_token: str | None = None
        self.systems: list[System] = []
        self.token: str | None = None
        self.webservers: list[WebServer] = []
        self.zones: list[Zone] = []

    async def api_request(
        self, method: str, path: str, json: Any | None = None
    ) -> dict[str, Any]:
        """Airzone Cloud API request."""
        _LOGGER.debug("aiohttp request: /%s (params=%s)", path, json)
        headers: dict[str, str] = {}
        if self.token:
            headers[HEADER_AUTHORIZATION] = f"{HEADER_BEARER} {self.token}"
        resp: ClientResponse = await self.aiohttp_session.request(
            method,
            f"{API_URL}/{path}",
            headers=headers,
            json=json,
            raise_for_status=True,
            timeout=HTTP_CALL_TIMEOUT,
        )
        resp_json = await resp.json(content_type=None)
        _LOGGER.debug("aiohttp response: %s", resp_json)
        return cast(dict, resp_json)

    async def api_get_device_config(self, device: Device) -> dict[str, Any]:
        """Request API device config data."""
        dev_id = urllib.parse.quote(device.get_id())

        params = {
            API_INSTALLATION_ID: device.get_installation(),
        }
        dev_params = urllib.parse.urlencode(params)

        return await self.api_request(
            "GET",
            f"{API_V1}/{API_DEVICES}/{dev_id}/{API_CONFIG}?{dev_params}",
        )

    async def api_get_device_status(self, device: Device) -> dict[str, Any]:
        """Request API device status data."""
        dev_id = urllib.parse.quote(device.get_id())

        params = {
            API_INSTALLATION_ID: device.get_installation(),
        }
        dev_params = urllib.parse.urlencode(params)

        return await self.api_request(
            "GET",
            f"{API_V1}/{API_DEVICES}/{dev_id}/{API_STATUS}?{dev_params}",
        )

    async def api_get_installation(self, installation: Installation) -> dict[str, Any]:
        """Request API installation data."""
        inst_id = urllib.parse.quote(installation.get_id())
        return await self.api_request(
            "GET",
            f"{API_V1}/{API_INSTALLATIONS}/{inst_id}",
        )

    async def api_get_installations(self) -> dict[str, Any]:
        """Request API installations data."""
        return await self.api_request(
            "GET",
            f"{API_V1}/{API_INSTALLATIONS}",
        )

    async def api_get_user(self) -> dict[str, Any]:
        """Request API user data."""
        return await self.api_request(
            "GET",
            f"{API_V1}/{API_USER}",
        )

    async def api_get_webserver(
        self, webserver: WebServer, devices: bool
    ) -> dict[str, Any]:
        """Request API webserver data."""
        ws_id = urllib.parse.quote(webserver.get_id())

        params: dict[str, Any] = {
            API_INSTALLATION_ID: webserver.get_installation(),
        }
        if devices:
            params[API_DEVICES] = 1
        ws_params = urllib.parse.urlencode(params)

        return await self.api_request(
            "GET",
            f"{API_V1}/{API_DEVICES}/{API_WS}/{ws_id}/{API_STATUS}?{ws_params}",
        )

    async def login(self) -> None:
        """Perform Airzone Cloud API login."""
        if self.token:
            self.logout()
        resp = await self.api_request(
            "POST",
            f"{API_V1}/{API_AUTH_LOGIN}",
            {
                API_EMAIL: self.options.username,
                API_PASSWORD: self.options.password,
            },
        )
        _LOGGER.debug("login resp: %s", resp)
        if resp.keys() < {API_TOKEN, API_REFRESH_TOKEN}:
            raise LoginError
        self.token = resp[API_TOKEN]
        self.refresh_token = resp[API_REFRESH_TOKEN]

    async def logout(self) -> None:
        """Perform Airzone Cloud API logout."""
        try:
            if self.token:
                await self.api_request(
                    "GET",
                    f"{API_V1}/{API_USER_LOGOUT}",
                )
        except ClientConnectorError:
            pass
        finally:
            self.refresh_token = None
            self.token = None

    async def token_refresh(self) -> None:
        """Perform Airzone Cloud API token refresh."""
        if self.token and self.refresh_token:
            resp = await self.api_request(
                "POST",
                f"{API_V1}/{API_AUTH_REFRESH_TOKEN}",
                {
                    API_REFRESH_TOKEN: self.refresh_token,
                },
            )
            _LOGGER.debug("refresh resp: %s", resp)
            if resp.keys() < {API_TOKEN, API_REFRESH_TOKEN}:
                raise TokenRefreshError
            self.token = resp[API_TOKEN]
            self.refresh_token = resp[API_REFRESH_TOKEN]

    def data(self) -> dict[str, Any]:
        """Return Airzone Cloud data."""
        data: dict[str, Any] = {}

        if self.installations:
            installations: dict[str, Any] = {}
            for installation in self.installations:
                installations[installation.get_id()] = installation.data()
            data[AZD_INSTALLATIONS] = installations

        if self.systems:
            systems: dict[str, Any] = {}
            for system in self.systems:
                systems[system.get_id()] = system.data()
            data[AZD_SYSTEMS] = systems

        if self.webservers:
            webservers: dict[str, Any] = {}
            for webserver in self.webservers:
                webservers[webserver.get_id()] = webserver.data()
            data[AZD_WEBSERVERS] = webservers

        if self.zones:
            zones: dict[str, Any] = {}
            for zone in self.zones:
                zones[zone.get_id()] = zone.data()
            data[AZD_ZONES] = zones

        return data

    def get_installation_id(self, inst_id: str) -> Installation | None:
        """Return Airzone Cloud Installation by ID."""
        for inst in self.installations:
            if inst_id == inst.get_id():
                return inst
        return None

    def get_system_id(self, sys_id: str) -> System | None:
        """Return Airzone Cloud System by ID."""
        for system in self.systems:
            if sys_id == system.get_id():
                return system
        return None

    def get_webserver_id(self, ws_id: str) -> WebServer | None:
        """Return Airzone Cloud WebServer by ID."""
        for ws in self.webservers:
            if ws_id == ws.get_id():
                return ws
        return None

    def get_zone_id(self, zone_id: str) -> Zone | None:
        """Return Airzone Cloud Zone by ID."""
        for zone in self.zones:
            if zone_id == zone.get_id():
                return zone
        return None

    async def update_installations(self) -> None:
        """Update Airzone Cloud installations from API."""
        installations_data = await self.api_get_installations()
        for installation_data in installations_data[API_INSTALLATIONS]:
            if not self.get_installation_id(installation_data[API_INSTALLATION_ID]):
                installation = Installation(installation_data)
                if installation:
                    self.installations.append(installation)
                    for ws_id in installation.get_webservers():
                        if not self.get_webserver_id(ws_id):
                            ws = WebServer(installation.get_id(), ws_id)
                            self.webservers.append(ws)

    async def update_system(self, system: System) -> None:
        """Update Airzone Cloud System from API."""
        device_data = await self.api_get_device_status(system)
        system.update(device_data)

    async def update_system_id(self, sys_id: str) -> None:
        """Update Airzone Cloud System by ID."""
        system = self.get_system_id(sys_id)
        if system:
            await self.update_system(system)

    async def update_systems(self) -> None:
        """Update all Airzone Cloud Systems."""
        for system in self.systems:
            await self.update_system(system)

    async def update_webserver(self, ws: WebServer, devices: bool) -> None:
        """Update Airzone Cloud WebServer from API."""
        ws_data = await self.api_get_webserver(ws, devices)
        ws.update(ws_data)
        if devices:
            for device_data in ws_data[API_DEVICES]:
                if API_AZ_ZONE == device_data[API_DEVICE_TYPE]:
                    if not self.get_zone_id(device_data[API_DEVICE_ID]):
                        zone = Zone(ws.get_installation(), ws.get_id(), device_data)
                        if zone:
                            self.zones.append(zone)
                elif API_AZ_SYSTEM == device_data[API_DEVICE_TYPE]:
                    if not self.get_zone_id(device_data[API_DEVICE_ID]):
                        system = System(ws.get_installation(), ws.get_id(), device_data)
                        if system:
                            self.systems.append(system)

    async def update_webserver_id(self, ws_id: str, devices: bool = False) -> None:
        """Update Airzone Cloud WebServer by ID."""
        ws = self.get_webserver_id(ws_id)
        if ws:
            await self.update_webserver(ws, devices)

    async def update_webservers(self, devices: bool = True) -> None:
        """Update all Airzone Cloud WebServers."""
        for ws in self.webservers:
            await self.update_webserver(ws, devices)

    async def update_zone(self, zone: Zone) -> None:
        """Update Airzone Cloud Zone from API."""
        device_data = await self.api_get_device_status(zone)
        zone.update(device_data)

    async def update_zone_id(self, zone_id: str) -> None:
        """Update Airzone Cloud Zone by ID."""
        zone = self.get_zone_id(zone_id)
        if zone:
            await self.update_zone(zone)

    async def update_zones(self) -> None:
        """Update all Airzone Cloud Zones."""
        for zone in self.zones:
            await self.update_zone(zone)
