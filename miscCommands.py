from aiohttp import ClientSession
from json import loads
from discord import Embed

import helperFunctions

# Misc commands

async def miscPlayerCount(client,channel):
    async with ClientSession() as session:
        embed = Embed(title="Shotbow", description="Player numbers", color=0xede351)
        data = await helperFunctions.fetch(session,'https://shotbow.net/serverList.json')
        d = loads(data)
        for key,value in d.items():
            try:
                if int(value) < 1:
                    continue
                if "us" in str(key) or "ddg" in str(key):
                    continue
            except:
                pass
            embed.add_field(name=str(key).capitalize(), value=str(value), inline=False)
        await client.send_message(channel,embed=embed)
