"""Raw Airzone Cloud API data example."""
import asyncio
import json
import timeit

import _secrets
import aiohttp

from aioairzone_cloud.cloudapi import AirzoneCloudApi
from aioairzone_cloud.exceptions import LoginError, TooManyRequests


async def main():
    """Raw Airzone Cloud API data example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AirzoneCloudApi(aiohttp_session, _secrets.AIRZONE_OPTIONS)

        try:
            await client.login()

            user_data = await client.api_get_user()
            print(json.dumps(user_data, indent=4, sort_keys=True))
            print("***")

            inst_list = await client.list_installations()
            for inst in inst_list:
                print(json.dumps(inst.data(), indent=4, sort_keys=True))
            client.select_installation(inst_list[0])
            await client.update_installation(inst_list[0])
            print("***")

            update_start = timeit.default_timer()
            await client.update()
            update_end = timeit.default_timer()
            print(json.dumps(client.data(), indent=4, sort_keys=True))
            print(f"Update time: {update_end - update_start}")
            print("***")

            print(json.dumps(client.raw_data(), indent=4, sort_keys=True))

            await client.logout()
        except LoginError:
            print("Login error.")
        except TooManyRequests:
            print("Too many requests.")


if __name__ == "__main__":
    asyncio.run(main())
