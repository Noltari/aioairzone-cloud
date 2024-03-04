"""Airzone Cloud API Token."""

from __future__ import annotations

from datetime import datetime
from typing import Any
import urllib.parse

from .const import (
    API_AUTH_REFRESH_TOKEN,
    API_REFRESH_TOKEN,
    API_TOKEN,
    API_V1,
    HEADER_AUTHORIZATION,
    HEADER_BEARER,
    TOKEN_REFRESH_PERIOD,
    WS_JWT,
)
from .exceptions import LoginError, TokenRefreshError


class AirzoneCloudToken:
    """Airzone Cloud Token."""

    def __init__(self) -> None:
        """Airzone Cloud Token init."""
        self.refresh_time: datetime | None = None
        self.refresh_token: str | None = None
        self.token: str | None = None

    def check_refresh(self) -> bool:
        """Check if Airzone Cloud Token needs refreshing."""
        return (
            self.refresh_time is not None
            and (datetime.now() - self.refresh_time) >= TOKEN_REFRESH_PERIOD
        )

    def clear(self) -> None:
        """Clear Airzone Cloud Token."""
        self.refresh_time = None
        self.refresh_token = None
        self.token = None

    def headers(self) -> dict[str, Any]:
        """Airzone Cloud Token headers."""
        _headers: dict[str, Any] = {}

        if self.token is not None:
            _headers[HEADER_AUTHORIZATION] = f"{HEADER_BEARER} {self.token}"

        return _headers

    def is_valid(self) -> bool:
        """Check if Airzone Cloud Token is valid."""
        return (
            self.refresh_time is not None
            and self.refresh_token is not None
            and self.token is not None
        )

    def jwt(self) -> dict[str, Any]:
        """Airzone Cloud WebSockets headers."""
        _jwt: dict[str, Any] = {}

        if self.token is not None:
            _jwt[WS_JWT] = self.token

        return _jwt

    def update(self, resp: dict[str, Any], refresh: bool) -> None:
        """Update Airzone Cloud Token."""
        refresh_token = resp.get(API_REFRESH_TOKEN)
        token = resp.get(API_TOKEN)

        if refresh_token is None or token is None:
            if refresh:
                raise TokenRefreshError("Invalid API response")
            raise LoginError("Invalid API response")

        self.refresh_time = datetime.now()
        self.refresh_token = refresh_token
        self.token = token

    def url_refresh(self) -> str:
        """Airzone Cloud Token refresh URL."""
        refresh_token = urllib.parse.quote(self.refresh_token or "")
        return f"{API_V1}/{API_AUTH_REFRESH_TOKEN}/{refresh_token}"
