"""Airzone Cloud token refresh example."""
import asyncio
import json

import _secrets
import aiohttp

from aioairzone_cloud.cloudapi import AirzoneCloudApi
from aioairzone_cloud.exceptions import LoginError, TokenRefreshError, TooManyRequests


async def main():
    """Airzone Cloud token refresh example."""

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
            print("***")

            await client.update_webservers(True)
            await client.update_systems()
            await client.update_zones()
            print(json.dumps(client.data(), indent=4, sort_keys=True))
            print("***")

            await client.token_refresh()

            await client.update_webservers(False)
            await client.update_systems()
            await client.update_zones()
            print(json.dumps(client.data(), indent=4, sort_keys=True))

            await client.logout()
        except TokenRefreshError:
            print("Token refresh error.")
        except LoginError:
            print("Login error.")
        except TooManyRequests:
            print("Too many requests.")


if __name__ == "__main__":
    asyncio.run(main())
