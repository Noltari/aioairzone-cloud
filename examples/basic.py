"""Basic Airzone Cloud client example."""
import asyncio
import json

import _secrets
import aiohttp

from aioairzone_cloud.cloudapi import AirzoneCloudApi


async def main():
    """Basic Airzone client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AirzoneCloudApi(aiohttp_session, _secrets.AIRZONE_OPTIONS)
        await client.login()

        user_data = await client.api_get_user()
        print(json.dumps(user_data, indent=4, sort_keys=True))
        print("***")

        await client.update_installations()
        await client.update_webservers()
        await client.update_systems()
        await client.update_zones()
        print(json.dumps(client.data(), indent=4, sort_keys=True))

        await client.logout()


if __name__ == "__main__":
    asyncio.run(main())
