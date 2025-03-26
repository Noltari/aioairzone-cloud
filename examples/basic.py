"""Basic Airzone Cloud client example."""

import asyncio
import json
import timeit
from typing import Any

from _secrets import AIRZONE_OPTIONS
import aiohttp

from aioairzone_cloud.cloudapi import AirzoneCloudApi
from aioairzone_cloud.exceptions import LoginError, TooManyRequests


def update_callback(data: dict[str, Any]) -> None:
    """Update callback function."""
    print(f"update_callback: data_len={len(data)}")


async def main():
    """Basic Airzone client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AirzoneCloudApi(aiohttp_session, AIRZONE_OPTIONS)

        client.set_update_callback(update_callback)

        try:
            await client.login()

            user_data = await client.api_get_user()
            print(json.dumps(user_data, indent=4, sort_keys=True))
            print("***")

            inst_list = await client.list_installations()
            for inst in inst_list:
                print(json.dumps(inst.data(), indent=4, sort_keys=True))
            await client.update_installations()
            await client.update_webservers(True)
            print("***")

            update_start = timeit.default_timer()
            await client.update()
            update_end = timeit.default_timer()
            print(json.dumps(client.data(), indent=4, sort_keys=True))
            print(f"Update time: {update_end - update_start}")

            await client.logout()
        except LoginError:
            print("Login error.")
        except TooManyRequests:
            print("Too many requests.")


if __name__ == "__main__":
    asyncio.run(main())
