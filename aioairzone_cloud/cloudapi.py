"""Airzone Cloud API."""
from __future__ import annotations

import asyncio
import logging
import urllib.parse
from datetime import datetime
from typing import Any, cast

from aiohttp import ClientConnectorError, ClientResponseError, ClientSession
from aiohttp.client_reqrep import ClientResponse

from .aidoo import Aidoo
from .common import ConnectionOptions
from .const import (
    API_AUTH_LOGIN,
    API_AUTH_REFRESH_TOKEN,
    API_AZ_AIDOO,
    API_AZ_SYSTEM,
    API_AZ_ZONE,
    API_CONFIG,
    API_DEVICE_ID,
    API_DEVICE_TYPE,
    API_DEVICES,
    API_EMAIL,
    API_GROUPS,
    API_INSTALLATION_ID,
    API_INSTALLATIONS,
    API_PASSWORD,
    API_REFRESH_TOKEN,
    API_STATUS,
    API_TOKEN,
    API_TYPE,
    API_URL,
    API_USER,
    API_USER_LOGOUT,
    API_V1,
    API_WS,
    API_WS_ID,
    AZD_AIDOOS,
    AZD_INSTALLATIONS,
    AZD_SYSTEMS,
    AZD_WEBSERVERS,
    AZD_ZONES,
    HEADER_AUTHORIZATION,
    HEADER_BEARER,
    HTTP_CALL_TIMEOUT,
    RAW_DEVICES_CONFIG,
    RAW_DEVICES_STATUS,
    RAW_INSTALLATIONS,
    RAW_INSTALLATIONS_LIST,
    RAW_USER,
    RAW_WEBSERVERS,
    TOKEN_REFRESH_PERIOD,
)
from .device import Device
from .exceptions import (
    AirzoneCloudError,
    APIError,
    AuthError,
    LoginError,
    TokenRefreshError,
    TooManyRequests,
)
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
        self._api_raw_data: dict[str, Any] = {
            RAW_DEVICES_CONFIG: {},
            RAW_DEVICES_STATUS: {},
            RAW_INSTALLATIONS: {},
            RAW_WEBSERVERS: {},
        }
        self.aidoos: dict[str, Aidoo] = {}
        self.aiohttp_session = aiohttp_session
        self.installations: dict[str, Installation] = {}
        self.options = options
        self.refresh_time: datetime | None = None
        self.refresh_token: str | None = None
        self.systems: dict[str, System] = {}
        self.token: str | None = None
        self.webservers: dict[str, WebServer] = {}
        self.zones: dict[str, Zone] = {}

    async def api_request(
        self, method: str, path: str, json: Any | None = None
    ) -> dict[str, Any]:
        """Airzone Cloud API request."""
        _LOGGER.debug("aiohttp request: /%s (params=%s)", path, json)

        headers: dict[str, str] = {}
        if self.token is not None:
            headers[HEADER_AUTHORIZATION] = f"{HEADER_BEARER} {self.token}"

        try:
            resp: ClientResponse = await self.aiohttp_session.request(
                method,
                f"{API_URL}/{path}",
                headers=headers,
                json=json,
                raise_for_status=True,
                timeout=HTTP_CALL_TIMEOUT,
            )
        except ClientConnectorError as err:
            raise AirzoneCloudError(err) from err
        except ClientResponseError as err:
            if path.endswith(API_AUTH_LOGIN):
                raise LoginError(err) from err
            if path.endswith(API_AUTH_REFRESH_TOKEN):
                raise TokenRefreshError(err) from err

            if err.status == 400:
                raise APIError(err) from err
            if err.status == 401:
                raise AuthError(err) from err
            if err.status == 429:
                raise TooManyRequests(err) from err

            raise AirzoneCloudError(err) from err

        resp_json = await resp.json(content_type=None)
        _LOGGER.debug("aiohttp response: %s", resp_json)

        return cast(dict[str, Any], resp_json)

    async def api_get_device_config(self, device: Device) -> dict[str, Any]:
        """Request API device config data."""
        dev_id = device.get_id()
        url_id = urllib.parse.quote(dev_id)

        params = {
            API_INSTALLATION_ID: device.get_installation(),
        }
        dev_params = urllib.parse.urlencode(params)

        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_DEVICES}/{url_id}/{API_CONFIG}?{dev_params}",
        )
        self._api_raw_data[RAW_DEVICES_CONFIG][dev_id] = res

        return res

    async def api_get_device_status(self, device: Device) -> dict[str, Any]:
        """Request API device status data."""
        dev_id = device.get_id()
        url_id = urllib.parse.quote(dev_id)

        params = {
            API_INSTALLATION_ID: device.get_installation(),
        }
        dev_params = urllib.parse.urlencode(params)

        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_DEVICES}/{url_id}/{API_STATUS}?{dev_params}",
        )
        self._api_raw_data[RAW_DEVICES_STATUS][dev_id] = res

        return res

    async def api_get_installation(self, installation: Installation) -> dict[str, Any]:
        """Request API installation data."""
        inst_id = installation.get_id()
        url_id = urllib.parse.quote(inst_id)

        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_INSTALLATIONS}/{url_id}",
        )
        self._api_raw_data[RAW_INSTALLATIONS][inst_id] = res

        return res

    async def api_get_installations(self) -> dict[str, Any]:
        """Request API installations data."""
        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_INSTALLATIONS}",
        )
        self._api_raw_data[RAW_INSTALLATIONS_LIST] = res

        return res

    async def api_get_user(self) -> dict[str, Any]:
        """Request API user data."""
        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_USER}",
        )
        self._api_raw_data[RAW_USER] = res

        return res

    async def api_get_webserver(
        self, webserver: WebServer, devices: bool
    ) -> dict[str, Any]:
        """Request API webserver data."""
        ws_id = webserver.get_id()
        url_id = urllib.parse.quote(ws_id)

        params: dict[str, Any] = {
            API_INSTALLATION_ID: webserver.get_installation(),
        }
        if devices:
            params[API_DEVICES] = 1
        ws_params = urllib.parse.urlencode(params)

        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_DEVICES}/{API_WS}/{url_id}/{API_STATUS}?{ws_params}",
        )
        self._api_raw_data[RAW_WEBSERVERS][ws_id] = res

        return res

    async def login(self) -> None:
        """Perform Airzone Cloud API login."""
        if self.token is not None:
            await self.logout()
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
            raise LoginError("Invalid API response")
        self.refresh_time = datetime.now()
        self.refresh_token = resp[API_REFRESH_TOKEN]
        self.token = resp[API_TOKEN]

    async def logout(self) -> None:
        """Perform Airzone Cloud API logout."""
        try:
            if self.token is not None:
                await self.api_request(
                    "GET",
                    f"{API_V1}/{API_USER_LOGOUT}",
                )
        except AirzoneCloudError:
            pass
        finally:
            self.refresh_time = None
            self.refresh_token = None
            self.token = None

    async def token_refresh(self) -> None:
        """Perform Airzone Cloud API token refresh."""
        if self.token is not None and self.refresh_token is not None:
            refresh_token = urllib.parse.quote(self.refresh_token)
            resp = await self.api_request(
                "GET",
                f"{API_V1}/{API_AUTH_REFRESH_TOKEN}/{refresh_token}",
            )
            _LOGGER.debug("refresh resp: %s", resp)
            if resp.keys() < {API_TOKEN, API_REFRESH_TOKEN}:
                raise TokenRefreshError("Invalid API response")
            self.refresh_time = datetime.now()
            self.refresh_token = resp[API_REFRESH_TOKEN]
            self.token = resp[API_TOKEN]

    def raw_data(self) -> dict[str, Any]:
        """Return raw Airzone Cloud API data."""
        return self._api_raw_data

    def data(self) -> dict[str, Any]:
        """Return Airzone Cloud data."""
        data: dict[str, Any] = {}

        if len(self.aidoos) > 0:
            aidoos: dict[str, Any] = {}
            for key, aidoo in self.aidoos.items():
                aidoos[key] = aidoo.data()
            data[AZD_AIDOOS] = aidoos

        if len(self.installations) > 0:
            installations: dict[str, Any] = {}
            for key, installation in self.installations.items():
                installations[key] = installation.data()
            data[AZD_INSTALLATIONS] = installations

        if len(self.systems) > 0:
            systems: dict[str, Any] = {}
            for key, system in self.systems.items():
                systems[key] = system.data()
            data[AZD_SYSTEMS] = systems

        if len(self.webservers) > 0:
            webservers: dict[str, Any] = {}
            for key, webserver in self.webservers.items():
                webservers[key] = webserver.data()
            data[AZD_WEBSERVERS] = webservers

        if len(self.zones) > 0:
            zones: dict[str, Any] = {}
            for key, zone in self.zones.items():
                zones[key] = zone.data()
            data[AZD_ZONES] = zones

        return data

    def get_aidoo_id(self, aidoo_id: str) -> Aidoo | None:
        """Return Airzone Cloud Aidoo by ID."""
        return self.aidoos.get(aidoo_id)

    def get_installation_id(self, inst_id: str) -> Installation | None:
        """Return Airzone Cloud Installation by ID."""
        return self.installations.get(inst_id)

    def get_system_id(self, sys_id: str) -> System | None:
        """Return Airzone Cloud System by ID."""
        return self.systems.get(sys_id)

    def get_webserver_id(self, ws_id: str) -> WebServer | None:
        """Return Airzone Cloud WebServer by ID."""
        return self.webservers.get(ws_id)

    def get_zone_id(self, zone_id: str) -> Zone | None:
        """Return Airzone Cloud Zone by ID."""
        return self.zones.get(zone_id)

    async def list_installations(self) -> list[Installation]:
        """Return Airzone Cloud installations list."""
        inst_list: list[Installation] = []

        inst_data = await self.api_get_installations()
        for inst in inst_data[API_INSTALLATIONS]:
            inst_list += [Installation(inst)]

        return inst_list

    def select_installation(self, inst: Installation) -> None:
        """Select single Airzone Cloud installation."""
        self.installations = {
            inst.get_id(): inst,
        }
        for ws_id in inst.get_webservers():
            if self.get_webserver_id(ws_id) is None:
                self.webservers[ws_id] = WebServer(inst.get_id(), ws_id)

    def set_system_zones_data(self, system: System) -> None:
        """Set slave zones modes from master zone."""
        modes = system.get_modes()
        installation_id = system.get_installation()
        system_id = system.get_id()
        system_num = system.get_system()
        for zone in self.zones.values():
            if (
                zone.get_installation() != installation_id
                or zone.get_system() != system_num
            ):
                continue

            zone.set_system_id(system_id)
            if zone.get_master() is False and modes:
                zone.set_modes(modes)

    async def update_aidoo(self, aidoo: Aidoo) -> None:
        """Update Airzone Cloud Zone from API."""
        device_data = await self.api_get_device_status(aidoo)
        aidoo.update(device_data)

    async def update_aidoos(self) -> None:
        """Update all Airzone Cloud Aidoos."""
        tasks = []

        for aidoo in self.aidoos.values():
            tasks += [self.update_aidoo(aidoo)]

        await asyncio.gather(*tasks)

    async def update_installation(self, inst: Installation) -> None:
        """Update Airzone Cloud installation from API."""
        installation_data = await self.api_get_installation(inst)
        for group in installation_data[API_GROUPS]:
            for device_data in group[API_DEVICES]:
                if API_AZ_ZONE == device_data[API_TYPE]:
                    if self.get_zone_id(device_data[API_DEVICE_ID]) is None:
                        zone = Zone(inst.get_id(), device_data[API_WS_ID], device_data)
                        if zone is not None:
                            self.zones[zone.get_id()] = zone
                elif API_AZ_SYSTEM == device_data[API_TYPE]:
                    if self.get_system_id(device_data[API_DEVICE_ID]) is None:
                        system = System(
                            inst.get_id(), device_data[API_WS_ID], device_data
                        )
                        if system is not None:
                            self.systems[system.get_id()] = system
                elif API_AZ_AIDOO == device_data[API_TYPE]:
                    if self.get_aidoo_id(device_data[API_DEVICE_ID]) is None:
                        aidoo = Aidoo(
                            inst.get_id(), device_data[API_WS_ID], device_data
                        )
                        if aidoo is not None:
                            self.aidoos[aidoo.get_id()] = aidoo

    async def update_installations(self) -> None:
        """Update Airzone Cloud installations from API."""
        installations_data = await self.api_get_installations()
        for installation_data in installations_data[API_INSTALLATIONS]:
            if self.get_installation_id(installation_data[API_INSTALLATION_ID]) is None:
                installation = Installation(installation_data)
                if installation is not None:
                    self.installations[installation.get_id()] = installation
                    for ws_id in installation.get_webservers():
                        if self.get_webserver_id(ws_id) is None:
                            ws = WebServer(installation.get_id(), ws_id)
                            self.webservers[ws_id] = ws

    async def update_system(self, system: System) -> None:
        """Update Airzone Cloud System from API."""
        device_data = await self.api_get_device_status(system)
        system.update(device_data)

    async def update_system_id(self, sys_id: str) -> None:
        """Update Airzone Cloud System by ID."""
        system = self.get_system_id(sys_id)
        if system is not None:
            await self.update_system(system)

    async def update_systems(self) -> None:
        """Update all Airzone Cloud Systems."""
        tasks = []

        for system in self.systems.values():
            tasks += [self.update_system(system)]

        await asyncio.gather(*tasks)

    async def update_webserver(self, ws: WebServer, devices: bool) -> None:
        """Update Airzone Cloud WebServer from API."""
        ws_data = await self.api_get_webserver(ws, devices)
        ws.update(ws_data)
        if devices:
            for device_data in ws_data[API_DEVICES]:
                if API_AZ_ZONE == device_data[API_DEVICE_TYPE]:
                    if self.get_zone_id(device_data[API_DEVICE_ID]) is None:
                        zone = Zone(ws.get_installation(), ws.get_id(), device_data)
                        if zone is not None:
                            self.zones[zone.get_id()] = zone
                elif API_AZ_SYSTEM == device_data[API_DEVICE_TYPE]:
                    if self.get_system_id(device_data[API_DEVICE_ID]) is None:
                        system = System(ws.get_installation(), ws.get_id(), device_data)
                        if system is not None:
                            self.systems[system.get_id()] = system
                elif API_AZ_AIDOO == device_data[API_DEVICE_TYPE]:
                    if self.get_aidoo_id(device_data[API_DEVICE_ID]) is None:
                        aidoo = Aidoo(ws.get_installation(), ws.get_id(), device_data)
                        if aidoo is not None:
                            self.aidoos[aidoo.get_id()] = aidoo

    async def update_webserver_id(self, ws_id: str, devices: bool) -> None:
        """Update Airzone Cloud WebServer by ID."""
        ws = self.get_webserver_id(ws_id)
        if ws is not None:
            await self.update_webserver(ws, devices)

    async def update_webservers(self, devices: bool) -> None:
        """Update all Airzone Cloud WebServers."""
        tasks = []

        for ws in self.webservers.values():
            tasks += [self.update_webserver(ws, devices)]

        await asyncio.gather(*tasks)

    async def update_zone(self, zone: Zone) -> None:
        """Update Airzone Cloud Zone from API."""
        device_data = await self.api_get_device_status(zone)
        zone.update(device_data)

    async def update_zone_id(self, zone_id: str) -> None:
        """Update Airzone Cloud Zone by ID."""
        zone = self.get_zone_id(zone_id)
        if zone is not None:
            await self.update_zone(zone)

    async def update_zones(self) -> None:
        """Update all Airzone Cloud Zones."""
        tasks = []

        for zone in self.zones.values():
            tasks += [self.update_zone(zone)]

        await asyncio.gather(*tasks)

        for system in self.systems.values():
            self.set_system_zones_data(system)

    async def _update(self) -> None:
        tasks = [
            self.update_webservers(False),
            self.update_systems(),
            self.update_zones(),
            self.update_aidoos(),
        ]

        await asyncio.gather(*tasks)

    async def update(self) -> None:
        """Update all Airzone Cloud data."""

        if (self.refresh_time is not None) and (
            datetime.now() - self.refresh_time
        ) >= TOKEN_REFRESH_PERIOD:
            try:
                await self.token_refresh()
            except TokenRefreshError:
                await self.login()

        try:
            await self._update()
        except LoginError:
            await self.login()
            await self._update()
