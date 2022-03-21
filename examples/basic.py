"""Basic Airzone Cloud client example."""
import asyncio
import json

from aiohttp import ClientSession

from aioairzone_cloud.cloudapi import AirzoneCloudApi
from aioairzone_cloud.common import ConnectionOptions


async def main():
    """Basic Airzone client example."""

    options = ConnectionOptions("airzone_email", "airzone_password")
    async with ClientSession() as aiohttp_session:
        client = AirzoneCloudApi(aiohttp_session, options)
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
