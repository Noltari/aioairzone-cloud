"""Basic Airzone Cloud client example."""
import asyncio
import json

import _secrets
from aiohttp import ClientSession

from aioairzone_cloud.cloudapi import AirzoneCloudApi


async def main():
    """Basic Airzone client example."""

    async with ClientSession() as aiohttp_session:
        client = AirzoneCloudApi(aiohttp_session, _secrets.AIRZONE_OPTIONS)
        await client.login()

        user_data = await client.api_get_user()
        print(json.dumps(user_data, indent=4, sort_keys=True))
        print("***")

        inst_list = await client.list_installations()
        for inst in inst_list:
            print(json.dumps(inst.data(), indent=4, sort_keys=True))
        client.select_installation(inst_list[0])
        print("***")

        await client.update_webservers()
        await client.update_systems()
        await client.update_zones()
        print(json.dumps(client.data(), indent=4, sort_keys=True))

        await client.logout()


if __name__ == "__main__":
    asyncio.run(main())
