from aiohttp import ClientSession
from json import loads
from async_timeout import timeout

import helperFunctions

# Misc commands

async def miscPlayerCount(client,channel):
    async with ClientSession() as session:
        data = await helperFunctions.fetch(session,'https://shotbow.net/serverList.json')
        d = loads(data)
        servers = ""
        for key,value in d.items():
            try:
                if int(value) < 1:
                    continue
                if "us" in str(key) or "ddg" in str(key):
                    continue
            except:
                pass
            servers+=(str(key).upper()+" has "+str(value)+" online\n")
        await client.send_message(channel,("```"+servers+"```"))