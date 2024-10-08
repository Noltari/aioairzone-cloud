"""Change Airzone Cloud device parameters example."""

import asyncio
import json
import timeit

from _secrets import AIRZONE_INST, AIRZONE_OPTIONS
import aiohttp

from aioairzone_cloud.cloudapi import AirzoneCloudApi
from aioairzone_cloud.common import TemperatureUnit
from aioairzone_cloud.const import (
    API_OPTS,
    API_POWER,
    API_SETPOINT,
    API_UNITS,
    API_VALUE,
)
from aioairzone_cloud.exceptions import LoginError, TooManyRequests


async def main():
    """Change Airzone Cloud device parameters example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AirzoneCloudApi(aiohttp_session, AIRZONE_OPTIONS)

        try:
            await client.login()

            user_data = await client.api_get_user()
            print(json.dumps(user_data, indent=4, sort_keys=True))
            print("***")

            inst_list = await client.list_installations()
            for inst in inst_list:
                print(json.dumps(inst.data(), indent=4, sort_keys=True))
            client.select_installation(inst_list[AIRZONE_INST])
            await client.update_installation(inst_list[AIRZONE_INST])
            print("***")

            update_start = timeit.default_timer()
            await client.update()
            update_end = timeit.default_timer()
            print(json.dumps(client.data(), indent=4, sort_keys=True))
            print(f"Update time: {update_end - update_start}")

            await client.api_set_zone_id_params(
                list(client.zones)[0],
                {
                    API_POWER: {
                        API_VALUE: False,
                    },
                    API_SETPOINT: {
                        API_VALUE: 26,
                        API_OPTS: {
                            API_UNITS: TemperatureUnit.CELSIUS.value,
                        },
                    },
                },
            )

            await client.logout()
        except LoginError:
            print("Login error.")
        except TooManyRequests:
            print("Too many requests.")


if __name__ == "__main__":
    asyncio.run(main())
