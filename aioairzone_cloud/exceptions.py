"""Airzone Cloud API exceptions."""

from __future__ import annotations


class AirzoneCloudError(Exception):
    """Base class for Airzone Cloud errors."""


class AirzoneTimeout(AirzoneCloudError):
    """Exception raised when API times out."""


class APIError(AirzoneCloudError):
    """Exception raised when API fails."""


class LoginError(AirzoneCloudError):
    """Exception raised when login fails."""


class AuthError(LoginError):
    """Exception raised when API denies access."""


class TokenRefreshError(LoginError):
    """Exception raised when token refresh fails."""


class InvalidParam(AirzoneCloudError):
    """Exception raised when invalid param is requested."""


class ParamUpdateFailure(AirzoneCloudError):
    """Exception raised when parameter isn't updated."""


class TooManyRequests(AirzoneCloudError):
    """Exception raised when max API requests are exceeded."""


class UnprocessableEntity(AirzoneCloudError):
    """Exception raised when device is disconnected."""
