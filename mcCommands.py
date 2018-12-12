from aiohttp import ClientSession
from json import loads
from discord import Embed

import helperFunctions

async def name(client, channel, name):
    url='https://api.mojang.com/users/profiles/minecraft/'+name
    try:
        async with ClientSession() as session:
            embed = Embed(title=name, description=name+"'s past names are:", color=0xeee657)
            data=await helperFunctions.fetch(session,url)
            d=loads(data)
            ids=str(d['id'])
            url='https://api.mojang.com/user/profiles/'+ids+'/names'
            names=await helperFunctions.fetch(session,url)
            names=list(reversed(loads(names)))
            namesList = []
            for counter, item in enumerate(names):
                namesList.append(item['name'])
            output = ""
            for name in namesList:
                output += name+"\n"
            embed.add_field(name="Previous names", value=output ,inline=False)
            embed.add_field(name="More info in URL", value=url ,inline=False)
            await client.send_message(channel, embed=embed)
    except:
        await client.send_message(channel, 'No user exists with that name')

async def status(client,channel):
    async with ClientSession() as session:
        data=await helperFunctions.fetch(session,'https://status.mojang.com/check')
        d=loads(data)
        embed = Embed(title="Minecraft Server Status", description="Status of the Minecraft Servers", color=0xeee627)
        embed.add_field(name="Minecraft.net", value=str(d[0]["minecraft.net"]).capitalize(), inline=False)
        embed.add_field(name="Accounts Website", value=str(d[2]["account.mojang.com"]).capitalize(), inline=False)
        embed.add_field(name="Authorization Service", value=str(d[3]["authserver.mojang.com"]).capitalize(), inline=False)
        embed.add_field(name="Multiplayer Session Service", value=str(d[4]["sessionserver.mojang.com"]).capitalize(), inline=False)
        embed.add_field(name="Minecraft Skins", value=str(d[6]["textures.minecraft.net"]).capitalize(), inline=False)
        embed.add_field(name="Public API", value=str(d[5]["api.mojang.com"]).capitalize(), inline=False)

        await client.send_message(channel, embed=embed)

