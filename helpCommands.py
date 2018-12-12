from discord import Embed

# HELP COMMANDS
async def help(client, channel):
        embed = Embed(title="Help commands", description="Help Commands are:", color=0xeee657)
        embed.add_field(name=">wiki help", value="Lists commands for wiki", inline=False)
        embed.add_field(name=">mc help", value="Lists commands for mc", inline=False)
        embed.add_field(name=">reddit help", value="Lists commands for reddit", inline=False)
        embed.add_field(name=">twitter help", value="Lists commands for twitter", inline=False)
        embed.add_field(name=">rss help", value="Lists commands for rss/Shotbow Forum commands", inline=False)
        embed.add_field(name=">info", value="More information on the bot.", inline=False)
        await client.send_message(channel, embed=embed)

async def info(client, channel):
        embed = Embed(title="General Information", description="General Information on ShotBot project.", color=0xeee657)
        embed.add_field(name="Who it is developed by:", value="ODST: https://distortionlayers.neocities.org/", inline=False)
        embed.add_field(name="How you can support development:", value="Send me BTC or ETH.\nBTC: 1qaLaxJ2hD2o7xPwg53v9yciu53dAoaP9\nETH: 0x404BF5D3fbAA5D83780765aa7Af2F4FE18E4fFAE", inline=False)
        embed.add_field(name="Am I paid for this?", value="No.", inline=False)
        embed.add_field(name="Can I develop this with you?", value="Yes! This Bot is Open Source!\nhttps://github.com/Malod219/MZBot", inline=False)
        embed.add_field(name="Bugs/problems", value="PM me on discord ODST#7648, Will be patched if it is a bug/problem.", inline=False)
        await client.send_message(channel, embed=embed)

async def miscHelp(client, channel):
        embed = Embed(title="Misc Commands", description="Misc Commands are:", color=0xeee657)
        embed.add_field(name=">misc playercount", value="Gives a list of servers and the number online", inline=False)
        await client.send_message(channel, embed=embed)

async def mcHelp(client, channel):
    embed = Embed(title="Mc Commands", description="MC Commands are:", color=0xeee657)
    embed.add_field(name=">mc name [name]", value="Gives the past names of **name**", inline=False)
    embed.add_field(name=">mc status", value="Gives current minecraft server status", inline=False)
    await client.send_message(channel, embed=embed)

async def wikiHelp(client, channel):
        embed = Embed(title="Wiki Commands", description="Wiki Commands are:", color=0xeee657)

        embed.add_field(name=">wiki location [name]", value="Gives the general information of **name**", inline=False)
        embed.add_field(name=">wiki locationlist", value="Gives a list of all locations", inline=False)
        embed.add_field(name=">wiki coord [location]", value="Gives coordinates to a location", inline=False)
        embed.add_field(name=">wiki legendary [name]", value="Gives information on **name**. Note it have proper grammar.", inline=False)
        embed.add_field(name=">wiki legendarylist [type]", value="List legendaries for **type**. Type can be sword,bow,armour,misc,elite.", inline=False)
        await client.send_message(channel, embed=embed)