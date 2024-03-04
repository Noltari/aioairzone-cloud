"""Airzone Cloud API."""

from __future__ import annotations

import asyncio
from asyncio import Event, Lock, Task
from datetime import datetime
from json import JSONDecodeError, loads as json_loads
import logging
from typing import TYPE_CHECKING, Any
import urllib.parse

from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType

from .const import (
    API_DEVICE_ID,
    API_V1,
    API_WS_ID,
    WS_ALIVE_PERIOD,
    WS_AUTH,
    WS_BODY,
    WS_CORR_ID,
    WS_DEVICE_STATE,
    WS_DEVICE_STATE_END,
    WS_DEVICES_UPDATES,
    WS_EVENT,
    WS_INSTALLATION,
    WS_INSTALLATION_ID,
    WS_URL,
    WS_WEBSERVER_UPDATES,
    WS_WEBSOCKETS,
)
from .device import Device
from .entity import EntityUpdate, UpdateType
from .installation import Installation
from .token import AirzoneCloudToken

if TYPE_CHECKING:
    from .cloudapi import AirzoneCloudApi

_LOGGER = logging.getLogger(__name__)


class AirzoneCloudIWS:
    """Airzone Cloud Installation WebSockets."""

    def __init__(
        self,
        cloudapi: AirzoneCloudApi,
        installation: Installation,
    ):
        """Airzone Cloud WebSockets init."""
        self.alive_dt: datetime | None = None
        self.cloudapi: AirzoneCloudApi = cloudapi
        self.device_data_lock = Lock()
        self.device_data: dict[str, Any] = {}
        self.inst_id: str = installation.get_id()
        self.session: ClientSession = cloudapi.session or ClientSession()
        self.state_end: Event = Event()
        self.task: Task[None] | None = None
        self.token: AirzoneCloudToken = cloudapi.token

    async def _connect(self) -> None:
        """WebSockets connection."""
        params = {
            WS_INSTALLATION_ID: self.inst_id,
        }
        inst_params = urllib.parse.urlencode(params)
        url = f"{WS_URL}/{API_V1}/{WS_WEBSOCKETS}/{WS_INSTALLATION}?{inst_params}"

        await self.state_init()

        async with self.session.ws_connect(
            url,
            headers=self.token.headers(),
            autoclose=False,
            autoping=False,
        ) as ws:
            async for msg in ws:
                await self.handler(ws, msg)

    def connect(self) -> bool:
        """WebSockets task creation."""
        if self.task is not None:
            return self.is_connected()

        self.state_end.clear()
        self.task = asyncio.ensure_future(self._connect())

        return True

    def disconnect(self) -> bool:
        """WebSockets task deletion."""
        self.state_end.clear()

        task = self.task
        if task is None:
            return True

        res = task.cancel()
        self.task = None

        return res

    def reconnect(self) -> bool:
        """WebSockets reconnect."""
        _LOGGER.warning("WS[%s]: reconnecting...", self.inst_id)
        self.disconnect()
        return self.connect()

    def get_device_data(self, device: Device) -> dict[str, Any] | None:
        """Return WebSockets device data."""
        return self.device_data.get(device.get_id())

    async def handler_auth(
        self, ws: ClientWebSocketResponse, data: dict[str, Any]
    ) -> None:
        """WebSockets AUTH handler."""
        corr_id = data.get(WS_CORR_ID)
        if corr_id is not None:
            auth = {
                WS_CORR_ID: corr_id,
                WS_BODY: self.token.jwt(),
            }
            _LOGGER.debug("WS[%s]: AUTH[%s]", self.inst_id, corr_id)
            await ws.send_json(auth)
        else:
            _LOGGER.error("WS[%s]: AUTH error -> %s", self.inst_id, data)

    async def handler_close(self, ws: ClientWebSocketResponse) -> None:
        """WebSockets CLOSE handler."""
        _LOGGER.debug("WS[%s]: CLOSE", self.inst_id)
        await ws.close()

    async def handler_device_state(self, data: dict[str, Any]) -> None:
        """WebSockets DEVICE_STATE handler."""
        body: dict[str, Any] = data.get(WS_BODY, {})
        update = EntityUpdate(UpdateType.WS_FULL, body)
        dev_id: str | None = body.get(API_DEVICE_ID)

        _LOGGER.debug("WS[%s]: DEVICE_STATE[%s]", self.inst_id, dev_id)

        device = self.cloudapi.get_device_id(dev_id)
        if device is not None:
            async with self.device_data_lock:
                self.device_data[device.get_id()] = body

            await device.update(update)

    def handler_device_state_end(self, data: dict[str, Any]) -> None:
        """WebSockets DEVICE_STATE_END handler."""
        body: str | None = data.get(WS_BODY)

        if body == self.inst_id:
            _LOGGER.debug("WS[%s]: DEVICE_STATE_END", self.inst_id)
            self.state_end.set()
        else:
            _LOGGER.error("WS[%s]: DEVICE_STATE_END mismatch (%s)", self.inst_id, body)

    async def handler_devices_update(self, data: dict[str, Any]) -> None:
        """WebSockets DEVICES_UPDATES handler."""
        body: dict[str, Any] = data.get(WS_BODY, {})
        update = EntityUpdate(UpdateType.WS_PARTIAL, body)
        dev_id: str | None = body.get(API_DEVICE_ID)

        _LOGGER.debug("WS[%s]: DEVICES_UPDATES[%s]", self.inst_id, dev_id)

        device = self.cloudapi.get_device_id(dev_id)
        if device is not None:
            await device.update(update)

    async def handler_error(self, msg: WSMessage) -> None:
        """WebSockets ERROR handler."""
        _LOGGER.error("WS[%s]: ERROR -> %s", self.inst_id, msg)

    async def handler_ping(self, ws: ClientWebSocketResponse) -> None:
        """WebSockets PING handler."""
        _LOGGER.debug("WS[%s]: PING (%s)", self.inst_id, datetime.now())
        await ws.pong()

    async def handler_text(
        self, ws: ClientWebSocketResponse, data: dict[str, Any]
    ) -> None:
        """WebSockets TEXT handler."""
        event: str = data.get(WS_EVENT, "")
        if event == WS_AUTH:
            await self.handler_auth(ws, data)
        elif event == WS_DEVICE_STATE:
            await self.handler_device_state(data)
        elif event == WS_DEVICE_STATE_END:
            self.handler_device_state_end(data)
        elif event.startswith(WS_DEVICES_UPDATES):
            await self.handler_devices_update(data)
            self.cloudapi.update_callback()
        elif event.startswith(WS_WEBSERVER_UPDATES):
            await self.handler_webserver_updates(data)
            self.cloudapi.update_callback()
        else:
            _LOGGER.warning("WS[%s]: EVENT[%s] -> %s", self.inst_id, event, data)

    async def handler_webserver_updates(self, data: dict[str, Any]) -> None:
        """WebSockets WEBSERVER_UPDATES handler."""
        body: dict[str, Any] = data.get(WS_BODY, {})
        update = EntityUpdate(UpdateType.WS_PARTIAL, body)
        ws_id: str | None = body.get(API_WS_ID)

        _LOGGER.debug("WS[%s]: WEBSERVER_UPDATES[%s]", self.inst_id, ws_id)

        webserver = self.cloudapi.get_webserver_id(ws_id)
        if webserver is not None:
            await webserver.update(update)

    async def handler(self, ws: ClientWebSocketResponse, msg: WSMessage) -> None:
        """WebSockets message handler."""
        if msg.type == WSMsgType.TEXT:
            json_data = None
            try:
                json_data = json_loads(msg.data)
            except (JSONDecodeError, TypeError) as err:
                _LOGGER.error(err)

            if json_data is not None:
                self.set_alive()
                await self.handler_text(ws, json_data)
        elif msg.type == WSMsgType.PING:
            self.set_alive()
            await self.handler_ping(ws)
        elif msg.type == WSMsgType.CLOSE:
            await self.handler_close(ws)
        elif msg.type == WSMsgType.ERROR:
            await self.handler_error(msg)
        else:
            _LOGGER.warning("Unknown WS msg: %s", msg)

    def is_alive(self) -> bool:
        """WebSockets connection alive."""
        return (
            self.alive_dt is not None
            and (datetime.now() - self.alive_dt) <= WS_ALIVE_PERIOD
        )

    def is_connected(self) -> bool:
        """WebSockets connection status."""
        task = self.task

        if task is None:
            return False

        return not task.done()

    def set_alive(self) -> None:
        """WebSockets alive status update."""
        self.alive_dt = datetime.now()

    async def state_init(self) -> None:
        """WebSockets state init."""
        _LOGGER.debug("WS[%s]: DEVICE_STATE_INIT", self.inst_id)

        async with self.device_data_lock:
            self.device_data.clear()

        self.alive_dt = None
        self.state_end.clear()
