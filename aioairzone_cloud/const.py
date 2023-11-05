"""Airzone Cloud API constants."""

from datetime import timedelta
from typing import Final

API_ACTIVE: Final[str] = "active"
API_AUTH_LOGIN: Final[str] = "auth/login"
API_AUTH_REFRESH_TOKEN: Final[str] = "auth/refreshToken"
API_AUTO_MODE: Final[str] = "auto_mode"
API_CELSIUS: Final[str] = "celsius"
API_CITY: Final[str] = "city"
API_CONFIG: Final[str] = "config"
API_CONNECTION_DATE: Final[str] = "connection_date"
API_DEVICE_ID: Final[str] = "device_id"
API_DEVICE_TYPE: Final[str] = "device_type"
API_DEVICES: Final[str] = "devices"
API_DISCONNECTION_DATE: Final[str] = "disconnection_date"
API_ECO_CONF: Final[str] = "eco_conf"
API_EMAIL: Final[str] = "email"
API_ERRORS: Final[str] = "errors"
API_FAH: Final[str] = "fah"
API_GROUP: Final[str] = "group"
API_GROUP_ID: Final[str] = "group_id"
API_GROUPS: Final[str] = "groups"
API_HUMIDITY: Final[str] = "humidity"
API_INSTALLATION_ID: Final[str] = "installation_id"
API_INSTALLATIONS: Final[str] = "installations"
API_IS_CONNECTED: Final[str] = "isConnected"
API_LOCAL_TEMP: Final[str] = "local_temp"
API_LOCATION_ID: Final[str] = "location_id"
API_META: Final[str] = "meta"
API_MODE: Final[str] = "mode"
API_MODE_AVAIL: Final[str] = "mode_available"
API_NAME: Final[str] = "name"
API_OLD_ID: Final[str] = "_id"
API_OPTS: Final[str] = "opts"
API_PARAM: Final[str] = "param"
API_PARAMS: Final[str] = "params"
API_PASSWORD: Final[str] = "password"
API_PIN: Final[str] = "pin"
API_POWER: Final[str] = "power"
API_RANGE_MAX_AIR: Final[str] = "range_air_max"
API_RANGE_MIN_AIR: Final[str] = "range_air_min"
API_RANGE_SP_MAX_AUTO_AIR: Final[str] = "range_sp_auto_air_max"
API_RANGE_SP_MAX_COOL_AIR: Final[str] = "range_sp_cool_air_max"
API_RANGE_SP_MAX_DRY_AIR: Final[str] = "range_sp_dry_air_max"
API_RANGE_SP_MAX_EMERHEAT_AIR: Final[str] = "range_sp_emerheat_air_max"
API_RANGE_SP_MAX_HOT_AIR: Final[str] = "range_sp_hot_air_max"
API_RANGE_SP_MAX_STOP_AIR: Final[str] = "range_sp_stop_air_max"
API_RANGE_SP_MAX_VENT_AIR: Final[str] = "range_sp_vent_air_max"
API_RANGE_SP_MIN_AUTO_AIR: Final[str] = "range_sp_auto_air_min"
API_RANGE_SP_MIN_COOL_AIR: Final[str] = "range_sp_cool_air_min"
API_RANGE_SP_MIN_DRY_AIR: Final[str] = "range_sp_dry_air_min"
API_RANGE_SP_MIN_EMERHEAT_AIR: Final[str] = "range_sp_emerheat_air_min"
API_RANGE_SP_MIN_HOT_AIR: Final[str] = "range_sp_hot_air_min"
API_RANGE_SP_MIN_STOP_AIR: Final[str] = "range_sp_stop_air_min"
API_RANGE_SP_MIN_VENT_AIR: Final[str] = "range_sp_vent_air_min"
API_REFRESH_TOKEN: Final[str] = "refreshToken"
API_SETPOINT: Final[str] = "setpoint"
API_SLEEP: Final[str] = "sleep"
API_SP_AIR_AUTO: Final[str] = "setpoint_air_auto"
API_SP_AIR_COOL: Final[str] = "setpoint_air_cool"
API_SP_AIR_DRY: Final[str] = "setpoint_air_dry"
API_SP_AIR_HEAT: Final[str] = "setpoint_air_heat"
API_SP_AIR_STOP: Final[str] = "setpoint_air_stop"
API_SP_AIR_VENT: Final[str] = "setpoint_air_vent"
API_SPEED_CONF: Final[str] = "speed_conf"
API_SPEED_TYPE: Final[str] = "speed_type"
API_SPEED_VALUES: Final[str] = "speed_values"
API_STAT_AP_MAC: Final[str] = "stat_ap_mac"
API_STAT_CHANNEL: Final[str] = "stat_channel"
API_STAT_QUALITY: Final[str] = "stat_quality"
API_STAT_RSSI: Final[str] = "stat_rssi"
API_STAT_SSID: Final[str] = "stat_ssid"
API_STATUS: Final[str] = "status"
API_STEP: Final[str] = "step"
API_SYSTEM_NUMBER: Final[str] = "system_number"
API_TIMER: Final[str] = "timer"
API_TOKEN: Final[str] = "token"
API_TYPE: Final[str] = "type"
API_UNITS: Final[str] = "units"
API_URL: Final[str] = "https://m.airzonecloud.com"
API_USER: Final[str] = "user"
API_USER_ID: Final[str] = "user_id"
API_USER_LOGOUT: Final[str] = "user/logout"
API_USER_MODE_CONF: Final[str] = "usermode_conf"
API_V1: Final[str] = "api/v1"
API_VALUE: Final[str] = "value"
API_WARNINGS: Final[str] = "warnings"
API_WS: Final[str] = "ws"
API_WS_CONNECTED: Final[str] = "ws_connected"
API_WS_FW: Final[str] = "ws_fw"
API_WS_ID: Final[str] = "ws_id"
API_WS_IDS: Final[str] = "ws_ids"
API_WS_TYPE: Final[str] = "ws_type"
API_ZONE_NUMBER: Final[str] = "zone_number"

API_AZ_AIDOO: Final[str] = "aidoo"
API_AZ_AIDOO_PRO: Final[str] = "aidoo_it"
API_AZ_SYSTEM: Final[str] = "az_system"
API_AZ_ZONE: Final[str] = "az_zone"

API_DEFAULT_TEMP_STEP: Final[float] = 0.5

AZD_ACTION: Final[str] = "action"
AZD_ACTIVE: Final[str] = "active"
AZD_AIDOOS: Final[str] = "aidoos"
AZD_AVAILABLE: Final[str] = "available"
AZD_CONNECTION_DATE: Final[str] = "connection-date"
AZD_DISCONNECTION_DATE: Final[str] = "disconnection-date"
AZD_ERRORS: Final[str] = "errors"
AZD_FIRMWARE: Final[str] = "firmware"
AZD_GROUPS: Final[str] = "groups"
AZD_HUMIDITY: Final[str] = "humidity"
AZD_ID: Final[str] = "id"
AZD_INSTALLATION: Final[str] = "installation"
AZD_INSTALLATIONS: Final[str] = "installations"
AZD_IS_CONNECTED: Final[str] = "is-connected"
AZD_MASTER: Final[str] = "master"
AZD_MODE: Final[str] = "mode"
AZD_MODE_AUTO: Final[str] = "mode-auto"
AZD_MODES: Final[str] = "modes"
AZD_NAME: Final[str] = "name"
AZD_NUM_DEVICES: Final[str] = "num-devices"
AZD_NUM_GROUPS: Final[str] = "num-groups"
AZD_POWER: Final[str] = "power"
AZD_PROBLEMS: Final[str] = "problems"
AZD_SPEED: Final[str] = "speed"
AZD_SPEEDS: Final[str] = "speeds"
AZD_SPEED_TYPE: Final[str] = "speed-type"
AZD_SYSTEM: Final[str] = "system"
AZD_SYSTEM_ID: Final[str] = "system-id"
AZD_SYSTEMS: Final[str] = "systems"
AZD_TEMP: Final[str] = "temperature"
AZD_TEMP_STEP: Final[str] = "temperature-step"
AZD_TEMP_SET: Final[str] = "temperature-setpoint"
AZD_TEMP_SET_AUTO_AIR: Final[str] = "temperature-setpoint-auto-air"
AZD_TEMP_SET_COOL_AIR: Final[str] = "temperature-setpoint-cool-air"
AZD_TEMP_SET_DRY_AIR: Final[str] = "temperature-setpoint-dry-air"
AZD_TEMP_SET_HOT_AIR: Final[str] = "temperature-setpoint-hot-air"
AZD_TEMP_SET_STOP_AIR: Final[str] = "temperature-setpoint-stop-air"
AZD_TEMP_SET_VENT_AIR: Final[str] = "temperature-setpoint-vent-air"
AZD_TEMP_SET_MAX: Final[str] = "temperature-setpoint-max"
AZD_TEMP_SET_MAX_AUTO_AIR: Final[str] = "temperature-setpoint-max-auto-air"
AZD_TEMP_SET_MAX_COOL_AIR: Final[str] = "temperature-setpoint-max-cool-air"
AZD_TEMP_SET_MAX_DRY_AIR: Final[str] = "temperature-setpoint-max-dry-air"
AZD_TEMP_SET_MAX_EMERHEAT_AIR: Final[str] = "temperature-setpoint-max-emerheat-air"
AZD_TEMP_SET_MAX_HOT_AIR: Final[str] = "temperature-setpoint-max-hot-air"
AZD_TEMP_SET_MAX_STOP_AIR: Final[str] = "temperature-setpoint-max-stop-air"
AZD_TEMP_SET_MAX_VENT_AIR: Final[str] = "temperature-setpoint-max-vent-air"
AZD_TEMP_SET_MIN_AUTO_AIR: Final[str] = "temperature-setpoint-min-auto-air"
AZD_TEMP_SET_MIN_COOL_AIR: Final[str] = "temperature-setpoint-min-cool-air"
AZD_TEMP_SET_MIN_DRY_AIR: Final[str] = "temperature-setpoint-min-dry-air"
AZD_TEMP_SET_MIN_EMERHEAT_AIR: Final[str] = "temperature-setpoint-min-emerheat-air"
AZD_TEMP_SET_MIN_HOT_AIR: Final[str] = "temperature-setpoint-min-hot-air"
AZD_TEMP_SET_MIN_STOP_AIR: Final[str] = "temperature-setpoint-min-stop-air"
AZD_TEMP_SET_MIN_VENT_AIR: Final[str] = "temperature-setpoint-min-vent-air"
AZD_TEMP_SET_MIN: Final[str] = "temperature-setpoint-min"
AZD_TYPE: Final[str] = "type"
AZD_WARNINGS: Final[str] = "warnings"
AZD_WEBSERVER: Final[str] = "web-server"
AZD_WEBSERVERS: Final[str] = "web-servers"
AZD_WIFI_CHANNEL: Final[str] = "wifi-channel"
AZD_WIFI_MAC: Final[str] = "wifi-mac"
AZD_WIFI_QUALITY: Final[str] = "wifi-quality"
AZD_WIFI_RSSI: Final[str] = "wifi-rssi"
AZD_WIFI_SSID: Final[str] = "wifi-ssid"
AZD_WS_CONNECTED: Final[str] = "ws-connected"
AZD_ZONE: Final[str] = "zone"
AZD_ZONES: Final[str] = "zones"

HEADER_AUTHORIZATION: Final[str] = "Authorization"
HEADER_BEARER: Final[str] = "Bearer"

HTTP_CALL_TIMEOUT: Final[int] = 45
HTTP_MAX_REQUESTS: Final[int] = 4

RAW_DEVICES_CONFIG: Final[str] = "devices-config"
RAW_DEVICES_STATUS: Final[str] = "devices-status"
RAW_INSTALLATIONS: Final[str] = "installations"
RAW_INSTALLATIONS_LIST: Final[str] = "installations-list"
RAW_USER: Final[str] = "user"
RAW_WEBSERVERS: Final[str] = "webservers"

TOKEN_REFRESH_PERIOD: Final[timedelta] = timedelta(hours=12)
