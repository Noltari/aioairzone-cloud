"""Airzone Cloud API."""

from __future__ import annotations

import asyncio
from asyncio import Lock, Semaphore
from collections.abc import Callable
import logging
from typing import Any, cast
import urllib.parse

from aiohttp import (
    ClientConnectorError,
    ClientResponseError,
    ClientSession,
    ClientTimeout,
)

from .aidoo import Aidoo
from .common import ConnectionOptions, OperationMode
from .const import (
    API_AUTH_LOGIN,
    API_AUTH_REFRESH_TOKEN,
    API_AZ_ACS,
    API_AZ_AIDOO,
    API_AZ_AIDOO_ACS,
    API_AZ_AIDOO_PRO,
    API_AZ_SYSTEM,
    API_AZ_ZONE,
    API_CONFIG,
    API_DEVICE_ID,
    API_DEVICE_TYPE,
    API_DEVICES,
    API_EMAIL,
    API_GROUP,
    API_GROUPS,
    API_INSTALLATION_ID,
    API_INSTALLATIONS,
    API_MODE,
    API_OPTS,
    API_PARAM,
    API_PARAMS,
    API_PASSWORD,
    API_STATUS,
    API_TYPE,
    API_TYPE_USER,
    API_URL,
    API_USER,
    API_USER_LOGOUT,
    API_V1,
    API_VALUE,
    API_WS,
    API_WS_ID,
    AZD_AIDOOS,
    AZD_GROUPS,
    AZD_HOT_WATERS,
    AZD_INSTALLATIONS,
    AZD_SYSTEMS,
    AZD_WEBSERVERS,
    AZD_ZONES,
    HTTP_CALL_TIMEOUT,
    HTTP_MAX_REQUESTS,
    RAW_DEVICES_CONFIG,
    RAW_DEVICES_STATUS,
    RAW_INSTALLATIONS,
    RAW_INSTALLATIONS_LIST,
    RAW_USER,
    RAW_WEBSERVERS,
    WS_INIT_TIMEOUT,
)
from .device import Device
from .entity import EntityUpdate, UpdateType
from .exceptions import (
    AirzoneCloudError,
    APIError,
    AuthError,
    LoginError,
    TokenRefreshError,
    TooManyRequests,
    UnprocessableEntity,
)
from .group import Group
from .hotwater import HotWater
from .installation import Installation
from .system import System
from .token import AirzoneCloudToken
from .webserver import WebServer
from .websockets import AirzoneCloudIWS
from .zone import Zone

_LOGGER = logging.getLogger(__name__)


class AirzoneCloudApi:
    """Airzone Cloud API."""

    callback_function: Callable[[dict[str, Any]], None] | None
    callback_lock: Lock

    def __init__(
        self,
        session: ClientSession,
        options: ConnectionOptions,
    ):
        """Airzone Cloud API init."""
        self._api_init_done: bool = False
        self._api_raw_data: dict[str, Any] = {
            RAW_DEVICES_CONFIG: {},
            RAW_DEVICES_STATUS: {},
            RAW_INSTALLATIONS: {},
            RAW_WEBSERVERS: {},
        }
        self._api_raw_data_lock = Lock()
        self._api_semaphore: Semaphore = Semaphore(HTTP_MAX_REQUESTS)
        self._api_timeout: ClientTimeout = ClientTimeout(total=HTTP_CALL_TIMEOUT)
        self.aidoos: dict[str, Aidoo] = {}
        self.callback_function = None
        self.callback_lock = Lock()
        self.devices: dict[str, Device] = {}
        self.dhws: dict[str, HotWater] = {}
        self.groups: dict[str, Group] = {}
        self.installations: dict[str, Installation] = {}
        self.options = options
        self.session = session
        self.systems: dict[str, System] = {}
        self.token: AirzoneCloudToken = AirzoneCloudToken()
        self.webservers: dict[str, WebServer] = {}
        self.websockets: dict[str, AirzoneCloudIWS] = {}
        self.zones: dict[str, Zone] = {}

    async def set_api_raw_data(
        self, key: str, subkey: str | None, data: dict[str, Any] | None
    ) -> None:
        """Save API raw data if not empty."""
        if data is not None:
            async with self._api_raw_data_lock:
                if subkey is None:
                    self._api_raw_data[key] = data
                else:
                    self._api_raw_data[key][subkey] = data

    async def api_request(
        self, method: str, path: str, json: Any | None = None
    ) -> dict[str, Any]:
        """Airzone Cloud API request."""
        _LOGGER.debug("aiohttp request: /%s (params=%s)", path, json)

        async with self._api_semaphore:
            try:
                async with self.session.request(
                    method,
                    f"{API_URL}/{path}",
                    headers=self.token.headers(),
                    json=json,
                    raise_for_status=True,
                    timeout=self._api_timeout,
                ) as resp:
                    resp_json = await resp.json(content_type=None)
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
                if err.status == 422:
                    raise UnprocessableEntity(err) from err
                if err.status == 429:
                    raise TooManyRequests(err) from err

                raise AirzoneCloudError(err) from err
            except TimeoutError as err:
                raise TimeoutError(err) from err

        _LOGGER.debug("aiohttp response: %s", resp_json)

        return cast(dict[str, Any], resp_json)

    async def api_get_device_config(self, device: Device) -> dict[str, Any]:
        """Request API device config data."""
        if not self.options.device_config:
            return {}

        dev_id = device.get_id()
        inst_id = device.get_installation()
        url_id = urllib.parse.quote(dev_id)

        inst = self.get_installation_id(inst_id)
        if inst is not None:
            request_type = inst.get_request_type()
        else:
            request_type = API_TYPE_USER

        params = {
            API_INSTALLATION_ID: inst_id,
            API_TYPE: request_type,
        }
        dev_params = urllib.parse.urlencode(params)

        try:
            res = await self.api_request(
                "GET",
                f"{API_V1}/{API_DEVICES}/{url_id}/{API_CONFIG}?{dev_params}",
            )
        except UnprocessableEntity:
            res = {}

        await self.set_api_raw_data(RAW_DEVICES_CONFIG, dev_id, res)

        return res

    async def api_get_device_status(self, device: Device) -> dict[str, Any]:
        """Request API device status data."""
        dev_id = device.get_id()
        inst_id = device.get_installation()
        url_id = urllib.parse.quote(dev_id)

        params = {
            API_INSTALLATION_ID: inst_id,
        }
        dev_params = urllib.parse.urlencode(params)

        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_DEVICES}/{url_id}/{API_STATUS}?{dev_params}",
        )
        await self.set_api_raw_data(RAW_DEVICES_STATUS, dev_id, res)

        return res

    async def api_get_installation(self, installation: Installation) -> dict[str, Any]:
        """Request API installation data."""
        inst_id = installation.get_id()
        url_id = urllib.parse.quote(inst_id)

        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_INSTALLATIONS}/{url_id}",
        )
        await self.set_api_raw_data(RAW_INSTALLATIONS, inst_id, res)

        return res

    async def api_get_installations(self) -> dict[str, Any]:
        """Request API installations data."""
        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_INSTALLATIONS}",
        )
        await self.set_api_raw_data(RAW_INSTALLATIONS_LIST, None, res)

        return res

    async def api_get_user(self) -> dict[str, Any]:
        """Request API user data."""
        res = await self.api_request(
            "GET",
            f"{API_V1}/{API_USER}",
        )
        await self.set_api_raw_data(RAW_USER, None, res)

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
        await self.set_api_raw_data(RAW_WEBSERVERS, ws_id, res)

        return res

    async def api_patch_device(
        self, device: Device, json: dict[str, Any]
    ) -> dict[str, Any]:
        """Perform a PATCH request to update device parameters."""
        dev_id = device.get_id()
        url_id = urllib.parse.quote(dev_id)

        return await self.api_request(
            "PATCH",
            f"{API_V1}/{API_DEVICES}/{url_id}",
            json,
        )

    async def api_put_group(self, group: Group, json: dict[str, Any]) -> dict[str, Any]:
        """Perform a PUT request to update group parameters."""
        grp_id = group.get_id()
        grp_url = urllib.parse.quote(grp_id)
        inst_id = group.get_installation()
        inst_url = urllib.parse.quote(inst_id)

        return await self.api_request(
            "PUT",
            f"{API_V1}/{API_INSTALLATIONS}/{inst_url}/{API_GROUP}/{grp_url}",
            json,
        )

    async def api_put_installation(
        self, inst: Installation, json: dict[str, Any]
    ) -> dict[str, Any]:
        """Perform a PUT request to update installation parameters."""
        inst_id = inst.get_id()
        inst_url = urllib.parse.quote(inst_id)

        return await self.api_request(
            "PUT",
            f"{API_V1}/{API_INSTALLATIONS}/{inst_url}",
            json,
        )

    def api_conv_special_mode(
        self, modes: list[OperationMode], mode: OperationMode
    ) -> OperationMode:
        """Convert Home Assistant Operation Mode into its corresponding API value."""
        if mode == OperationMode.COOLING:
            if OperationMode.COOLING_COMBINED in modes:
                mode = OperationMode.COOLING_COMBINED
            elif OperationMode.COOLING_AIR in modes:
                mode = OperationMode.COOLING_AIR
            elif OperationMode.COOLING_RADIANT in modes:
                mode = OperationMode.COOLING_RADIANT
        elif mode == OperationMode.HEATING:
            if OperationMode.HEAT_COMBINED in modes:
                mode = OperationMode.HEAT_COMBINED
            elif OperationMode.HEAT_AIR in modes:
                mode = OperationMode.HEAT_AIR
            elif OperationMode.HEAT_RADIANT in modes:
                mode = OperationMode.HEAT_RADIANT
            elif OperationMode.EMERGENCY_HEAT in modes:
                mode = OperationMode.EMERGENCY_HEAT
        return mode

    async def api_set_device_param(
        self, device: Device, param: str, data: dict[str, Any]
    ) -> None:
        """Set device parameter."""
        if param == API_MODE:
            modes = device.get_modes() or []
            if data[API_VALUE] not in modes:
                data[API_VALUE] = self.api_conv_special_mode(
                    modes, data[API_VALUE]
                ).value

            if isinstance(device, Zone) and not device.get_master():
                # Mode can't be changed on slave zones
                system = device.get_system()
                if system is not None:
                    device = system

        json = {
            API_PARAM: param,
            API_VALUE: data[API_VALUE],
            API_INSTALLATION_ID: device.get_installation(),
        }

        if API_OPTS in data:
            json[API_OPTS] = data[API_OPTS]

        await self.api_patch_device(device, json)

        device.set_param(param, data)

    async def api_set_device_params(
        self, device: Device, params: dict[str, Any]
    ) -> None:
        """Set device parameters."""
        tasks = []

        for param, data in params.items():
            tasks += [
                asyncio.create_task(self.api_set_device_param(device, param, data))
            ]

        await asyncio.gather(*tasks)

    async def api_set_group_params(self, group: Group, params: dict[str, Any]) -> None:
        """Set group parameters."""
        for key, value in params.get(API_PARAMS, {}).items():
            if key == API_MODE:
                modes = group.get_modes() or []
                if value not in modes:
                    params[API_PARAMS][key] = self.api_conv_special_mode(
                        modes, value
                    ).value

        await self.api_put_group(group, params)

        group.set_params(params)

    async def api_set_installation_params(
        self, inst: Installation, params: dict[str, Any]
    ) -> None:
        """Set installation parameters."""
        for key, value in params.get(API_PARAMS, {}).items():
            if key == API_MODE:
                modes = inst.get_modes() or []
                if value not in modes:
                    params[API_PARAMS][key] = self.api_conv_special_mode(
                        modes, value
                    ).value

        await self.api_put_installation(inst, params)

        inst.set_params(params)

    async def api_set_aidoo_id_params(
        self, aidoo_id: str, params: dict[str, Any]
    ) -> None:
        """Set aidoo parameters."""
        aidoo = self.get_aidoo_id(aidoo_id)
        if aidoo is not None:
            await self.api_set_device_params(aidoo, params)

    async def api_set_device_id_params(
        self, device_id: str, params: dict[str, Any]
    ) -> None:
        """Set device parameters."""
        device = self.get_device_id(device_id)
        if device is not None:
            await self.api_set_device_params(device, params)

    async def api_set_dhw_id_params(self, dhw_id: str, params: dict[str, Any]) -> None:
        """Set dhw parameters."""
        dhw = self.get_dhw_id(dhw_id)
        if dhw is not None:
            await self.api_set_device_params(dhw, params)

    async def api_set_group_id_params(
        self, group_id: str, params: dict[str, Any]
    ) -> None:
        """Set group parameters."""
        group = self.get_group_id(group_id)
        if group is not None:
            await self.api_set_group_params(group, params)

    async def api_set_installation_id_params(
        self, inst_id: str, params: dict[str, Any]
    ) -> None:
        """Set installation parameters."""
        inst = self.get_installation_id(inst_id)
        if inst is not None:
            await self.api_set_installation_params(inst, params)

    async def api_set_system_id_params(
        self, system_id: str, params: dict[str, Any]
    ) -> None:
        """Set system parameters."""
        system = self.get_system_id(system_id)
        if system is not None:
            await self.api_set_device_params(system, params)

    async def api_set_zone_id_params(
        self, zone_id: str, params: dict[str, Any]
    ) -> None:
        """Set zone parameters."""
        zone = self.get_zone_id(zone_id)
        if zone is not None:
            await self.api_set_device_params(zone, params)

    async def login(self) -> None:
        """Perform Airzone Cloud API login."""
        if self.token.is_valid():
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
        self.token.update(resp, False)

    async def logout(self) -> None:
        """Perform Airzone Cloud API logout."""
        for inst_ws in self.websockets.values():
            inst_ws.disconnect()

        try:
            if self.token.is_valid():
                await self.api_request(
                    "GET",
                    f"{API_V1}/{API_USER_LOGOUT}",
                )
        except AirzoneCloudError:
            pass
        finally:
            self.token.clear()

    async def token_refresh(self) -> None:
        """Perform Airzone Cloud API token refresh."""
        if self.token.is_valid():
            resp = await self.api_request(
                "GET",
                self.token.url_refresh(),
            )
            _LOGGER.debug("refresh resp: %s", resp)
            self.token.update(resp, True)

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

        if len(self.dhws) > 0:
            dhws: dict[str, Any] = {}
            for key, dhw in self.dhws.items():
                dhws[key] = dhw.data()
            data[AZD_HOT_WATERS] = dhws

        if len(self.groups) > 0:
            groups: dict[str, Any] = {}
            for key, group in self.groups.items():
                groups[key] = group.data()
            data[AZD_GROUPS] = groups

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

    def add_aidoo(self, aidoo: Aidoo) -> None:
        """Add Airzone Cloud Aidoo."""
        self.aidoos[aidoo.get_id()] = aidoo
        self.add_device(aidoo)

    def add_device(self, device: Device) -> None:
        """Add Airzone Cloud Device."""
        dev_id = device.get_id()
        if dev_id not in self.devices:
            self.devices[dev_id] = device

    def add_dhw(self, dhw: HotWater) -> None:
        """Add Airzone Cloud Domestic Hot Water."""
        self.dhws[dhw.get_id()] = dhw
        self.add_device(dhw)

    def add_system(self, system: System) -> None:
        """Add Airzone Cloud System."""
        self.systems[system.get_id()] = system
        self.add_device(system)

    def add_zone(self, zone: Zone) -> None:
        """Add Airzone Cloud System."""
        self.zones[zone.get_id()] = zone
        self.add_device(zone)

    def get_aidoo_id(self, aidoo_id: str) -> Aidoo | None:
        """Return Airzone Cloud Aidoo by ID."""
        return self.aidoos.get(aidoo_id)

    def get_device_id(self, dev_id: str | None) -> Device | None:
        """Return Airzone Cloud Device by ID."""
        if dev_id is not None:
            return self.devices.get(dev_id)
        return None

    def get_dhw_id(self, dhw_id: str) -> HotWater | None:
        """Return Airzone Cloud DHW by ID."""
        return self.dhws.get(dhw_id)

    def get_group_id(self, group_id: str) -> Group | None:
        """Return Airzone Cloud Group by ID."""
        return self.groups.get(group_id)

    def get_installation_id(self, inst_id: str) -> Installation | None:
        """Return Airzone Cloud Installation by ID."""
        return self.installations.get(inst_id)

    def get_system_id(self, sys_id: str) -> System | None:
        """Return Airzone Cloud System by ID."""
        return self.systems.get(sys_id)

    def get_webserver_id(self, ws_id: str | None) -> WebServer | None:
        """Return Airzone Cloud WebServer by ID."""
        if ws_id is not None:
            return self.webservers.get(ws_id)
        return None

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
        inst_id = inst.get_id()

        if self.options.websockets:
            for _inst in list(self.installations):
                inst_ws = self.websockets.get(_inst)
                if inst_ws is not None and inst_ws.disconnect():
                    self.websockets.pop(_inst)

            if inst_id not in self.websockets:
                self.websockets[inst_id] = AirzoneCloudIWS(self, inst)

        self.installations = {
            inst_id: inst,
        }

        for ws_id in inst.get_webservers():
            if self.get_webserver_id(ws_id) is None:
                self.webservers[ws_id] = WebServer(inst_id, ws_id)

    def set_system_zones_data(self, system: System) -> None:
        """Set slave zones modes from master zone."""
        modes = system.get_modes()
        installation_id = system.get_installation()
        system_num = system.get_system_num()
        system_ws = system.get_webserver()
        for zone in self.zones.values():
            if (
                zone.get_installation() != installation_id
                or zone.get_system_num() != system_num
                or zone.get_webserver() != system_ws
            ):
                continue

            system.add_zone(zone)
            zone.set_system(system)
            if zone.get_master() is False and modes:
                zone.set_modes(modes)

    async def update_aidoo(self, aidoo: Aidoo) -> None:
        """Update Airzone Cloud Aidoo from API."""
        config_task = asyncio.create_task(self.api_get_device_config(aidoo))
        status_task = asyncio.create_task(self.api_get_device_status(aidoo))

        config_data = await config_task
        status_data = await status_task

        update = EntityUpdate(UpdateType.API_FULL, config_data | status_data)

        await aidoo.update(update)

    async def update_aidoos(self) -> None:
        """Update all Airzone Cloud Aidoos."""
        tasks = []

        for aidoo in self.aidoos.values():
            tasks += [asyncio.create_task(self.update_aidoo(aidoo))]

        await asyncio.gather(*tasks)

    async def update_dhw(self, dhw: HotWater) -> None:
        """Update Airzone Cloud DHW from API."""
        status_task = asyncio.create_task(self.api_get_device_status(dhw))

        status_data = await status_task

        update = EntityUpdate(UpdateType.API_FULL, status_data)

        await dhw.update(update)

    async def update_dhws(self) -> None:
        """Update all Airzone Cloud DHWs."""
        tasks = []

        for dhw in self.dhws.values():
            tasks += [asyncio.create_task(self.update_dhw(dhw))]

        await asyncio.gather(*tasks)

    def connect_installation_websockets(self, inst_id: str) -> None:
        """Connect installation WebSockets."""
        if not self.options.websockets:
            return

        inst_ws = self.websockets.get(inst_id)
        if inst_ws is not None:
            inst_ws.connect()

    async def update_installation(self, inst: Installation) -> None:
        """Update Airzone Cloud installation from API."""
        inst_id = inst.get_id()
        installation_data = await self.api_get_installation(inst)
        for group_data in installation_data[API_GROUPS]:
            group = Group(inst_id, group_data)
            inst.add_group(group)
            self.groups[group.get_id()] = group
            for device_data in group_data[API_DEVICES]:
                device_id = device_data[API_DEVICE_ID]
                device_type = device_data[API_TYPE]
                if device_type == API_AZ_ZONE:
                    if self.get_zone_id(device_id) is None:
                        zone = Zone(inst_id, device_data[API_WS_ID], device_data)
                        if zone is not None:
                            self.add_zone(zone)
                            group.add_zone(zone)
                            inst.add_zone(zone)
                elif device_type == API_AZ_SYSTEM:
                    if self.get_system_id(device_id) is None:
                        system = System(inst_id, device_data[API_WS_ID], device_data)
                        if system is not None:
                            self.add_system(system)
                            group.add_system(system)
                            inst.add_system(system)
                elif device_type in [API_AZ_AIDOO, API_AZ_AIDOO_PRO]:
                    if self.get_aidoo_id(device_id) is None:
                        aidoo = Aidoo(inst_id, device_data[API_WS_ID], device_data)
                        if aidoo is not None:
                            self.add_aidoo(aidoo)
                            group.add_aidoo(aidoo)
                            inst.add_aidoo(aidoo)
                elif device_type in [API_AZ_ACS, API_AZ_AIDOO_ACS]:
                    if self.get_dhw_id(device_id) is None:
                        dhw = HotWater(inst_id, device_data[API_WS_ID], device_data)
                        if HotWater is not None:
                            self.add_dhw(dhw)
                            group.add_dhw(dhw)
                            inst.add_dhw(dhw)

        self.connect_installation_websockets(inst_id)

    async def update_installations(self) -> None:
        """Update Airzone Cloud installations from API."""
        installations_data = await self.api_get_installations()
        for installation_data in installations_data[API_INSTALLATIONS]:
            if self.get_installation_id(installation_data[API_INSTALLATION_ID]) is None:
                installation = Installation(installation_data)
                if installation is not None:
                    inst_id = installation.get_id()
                    self.installations[inst_id] = installation
                    for ws_id in installation.get_webservers():
                        if self.get_webserver_id(ws_id) is None:
                            ws = WebServer(inst_id, ws_id)
                            self.webservers[ws_id] = ws

    def get_ws_device_data(self, device: Device) -> dict[str, Any] | None:
        """Get WebSockets device data."""
        inst_id = device.get_installation()
        ws = self.websockets.get(inst_id)
        if ws is not None:
            return ws.get_device_data(device)
        return None

    async def update_system(self, system: System) -> None:
        """Update Airzone Cloud System from API."""
        config_task = asyncio.create_task(self.api_get_device_config(system))
        status_task = asyncio.create_task(self.api_get_device_status(system))

        config_data = await config_task
        status_data = await status_task

        update = EntityUpdate(UpdateType.API_FULL, config_data | status_data)

        await system.update(update)

    async def update_system_id(self, sys_id: str) -> None:
        """Update Airzone Cloud System by ID."""
        system = self.get_system_id(sys_id)
        if system is not None:
            await self.update_system(system)

    async def update_systems(self) -> None:
        """Update all Airzone Cloud Systems."""
        tasks = []

        for system in self.systems.values():
            tasks += [asyncio.create_task(self.update_system(system))]

        await asyncio.gather(*tasks)

    async def update_systems_zones(self) -> None:
        """Update all Airzone Cloud Systems/Zones."""
        await self.update_systems()
        await self.update_zones()

    async def update_webserver(self, ws: WebServer, devices: bool) -> None:
        """Update Airzone Cloud WebServer from API."""
        inst_id = ws.get_installation()
        inst = self.get_installation_id(inst_id)
        if inst and not inst.user_access.is_admin():
            return

        ws_data = await self.api_get_webserver(ws, devices)

        update = EntityUpdate(UpdateType.API_FULL, ws_data)

        await ws.update(update)
        if devices:
            ws_id = ws.get_id()
            inst = self.get_installation_id(ws.get_installation())
            for device_data in ws_data[API_DEVICES]:
                device_id = device_data[API_DEVICE_ID]
                device_type = device_data[API_DEVICE_TYPE]
                if device_type == API_AZ_ZONE:
                    if self.get_zone_id(device_id) is None:
                        zone = Zone(ws.get_installation(), ws_id, device_data)
                        if zone is not None:
                            self.add_zone(zone)
                            if inst is not None:
                                inst.add_zone(zone)
                elif device_type == API_AZ_SYSTEM:
                    if self.get_system_id(device_id) is None:
                        system = System(ws.get_installation(), ws_id, device_data)
                        if system is not None:
                            self.add_system(system)
                            if inst is not None:
                                inst.add_system(system)
                elif device_type in [API_AZ_AIDOO, API_AZ_AIDOO_PRO]:
                    if self.get_aidoo_id(device_id) is None:
                        aidoo = Aidoo(ws.get_installation(), ws_id, device_data)
                        if aidoo is not None:
                            self.add_aidoo(aidoo)
                            if inst is not None:
                                inst.add_aidoo(aidoo)
                elif device_type in [API_AZ_ACS, API_AZ_AIDOO_ACS]:
                    if self.get_dhw_id(device_id) is None:
                        dhw = HotWater(ws.get_installation(), ws_id, device_data)
                        if dhw is not None:
                            self.add_dhw(dhw)
                            if inst is not None:
                                inst.add_dhw(dhw)

    async def update_webserver_id(self, ws_id: str, devices: bool) -> None:
        """Update Airzone Cloud WebServer by ID."""
        ws = self.get_webserver_id(ws_id)
        if ws is not None:
            await self.update_webserver(ws, devices)

    async def update_webservers(self, devices: bool) -> None:
        """Update all Airzone Cloud WebServers."""
        tasks = []

        for ws in self.webservers.values():
            tasks += [asyncio.create_task(self.update_webserver(ws, devices))]

        await asyncio.gather(*tasks)

    async def update_zone(self, zone: Zone) -> None:
        """Update Airzone Cloud Zone from API."""
        config_task = asyncio.create_task(self.api_get_device_config(zone))
        status_task = asyncio.create_task(self.api_get_device_status(zone))

        config_data = await config_task
        status_data = await status_task

        update = EntityUpdate(UpdateType.API_FULL, config_data | status_data)

        await zone.update(update)

    async def update_zone_id(self, zone_id: str) -> None:
        """Update Airzone Cloud Zone by ID."""
        zone = self.get_zone_id(zone_id)
        if zone is not None:
            await self.update_zone(zone)

    async def update_zones(self) -> None:
        """Update all Airzone Cloud Zones."""
        tasks = []

        for zone in self.zones.values():
            tasks += [asyncio.create_task(self.update_zone(zone))]

        await asyncio.gather(*tasks)

        for system in self.systems.values():
            self.set_system_zones_data(system)

    async def _update_polling(self) -> None:
        """Perform a polling update of Airzone Cloud data."""
        tasks = [
            asyncio.create_task(self.update_webservers(False)),
            asyncio.create_task(self.update_systems_zones()),
            asyncio.create_task(self.update_aidoos()),
            asyncio.create_task(self.update_dhws()),
        ]

        await asyncio.gather(*tasks)

        self._api_init_done = True

    async def _update_websockets(self) -> bool:
        """Perform a websockets update of Airzone Cloud data."""
        if not self.options.websockets:
            return False

        ws_updated = True
        for websocket in self.websockets.values():
            if not websocket.is_alive():
                websocket.reconnect()
            try:
                await asyncio.wait_for(websocket.state_end.wait(), WS_INIT_TIMEOUT)
            except asyncio.TimeoutError:
                ws_updated = False
        return ws_updated

    async def _update(self) -> None:
        """Update Airzone Cloud data using websockets and fall back to polling."""
        if not self._api_init_done or not await self._update_websockets():
            await self._update_polling()

    async def update(self) -> None:
        """Update all Airzone Cloud data."""

        if self.token.check_refresh():
            try:
                await self.token_refresh()
            except TokenRefreshError:
                await self.login()

        try:
            await self._update()
        except LoginError:
            await self.login()
            await self._update()

    async def _update_callback(self) -> None:
        """Perform update callback."""
        if self.callback_function:
            async with self.callback_lock:
                self.callback_function(self.data())

    def update_callback(self) -> None:
        """Create update callback task."""
        if self.callback_function:
            asyncio.ensure_future(self._update_callback())

    def set_update_callback(
        self, callback_function: Callable[[dict[str, Any]], None]
    ) -> None:
        """Set update callback."""
        self.callback_function = callback_function
