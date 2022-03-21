"""Airzone Cloud API exceptions."""
from __future__ import annotations


class AirzoneCloudError(Exception):
    """Base class for Airzone Cloud errors."""


class APIError(AirzoneCloudError):
    """Exception raised when API fails."""


class LoginError(AirzoneCloudError):
    """Exception raised when login fails."""


class TokenRefreshError(AirzoneCloudError):
    """Exception raised when token refresh fails."""


class InvalidParam(AirzoneCloudError):
    """Exception raised when invalid param is requested."""


class ParamUpdateFailure(AirzoneCloudError):
    """Exception raised when parameter isn't updated."""
