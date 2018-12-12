from aiohttp import ClientSession
from json import loads

import helperFunctions

async def name(client, channel, name):
    url='https://api.mojang.com/users/profiles/minecraft/'+name
    try:
        async with ClientSession() as session:
            data=await helperFunctions.fetch(session,url)
            d=loads(data)
            ids=str(d['id'])
            url='https://api.mojang.com/user/profiles/'+ids+'/names'
            names=await helperFunctions.fetch(session,url)
            names=list(reversed(loads(names)))
            output='Current name : `'+ name + '`\nPrevious names:\n'
            for counter, item in enumerate(names):
                output+='`'+(names[counter]['name']+'`\n')
            await client.send_message(channel, output+'\nMore Info :` https://namemc.com/name/'+name+'`')
    except:
        await client.send_message(channel, 'No user exists with that name')

async def status(client,channel):
    async with ClientSession() as session:
        data=await helperFunctions.fetch(session,'https://status.mojang.com/check')
        d=loads(data)
        await client.send_message(channel, '```Minecraft.net - '+str(d[0]["minecraft.net"])+
                            '\nAccounts Website - '+str(d[2]["account.mojang.com"])+
                            '\nAuthorization Service - '+str(d[3]["authserver.mojang.com"])+
                            '\nMultiplayer Session Service - '+str(d[4]["sessionserver.mojang.com"])+
                            '\nMinecraft Skins - '+str(d[6]["textures.minecraft.net"])+
                            '\nPublic API - '+str(d[5]["api.mojang.com"])+'```')

