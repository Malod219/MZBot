import discord

from keep_alive import keep_alive
import credentials
import mcCommands
import startUpFunctions
import miscCommands
import helpCommands
import wikiCommands

with open("config.cfg", "r") as configFile:
    config = configFile.readlines()

client = discord.Client()

@client.event
async def on_ready():
    client.loop.create_task(startUpFunctions.rssWatch(client))
    client.loop.create_task(startUpFunctions.redditWatch(client, config))
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('Invitation to bring this to the server {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?bot_id={}&scope=bot&permissions=8'.format(client.user.id))
    await client.change_presence(game=discord.Game(name='MineZ'))

@client.event
async def on_message(message):
    if message.content.startswith(">help"):
        await helpCommands.help(client, message.channel)

    elif message.content.startswith(">info"):
        await helpCommands.info(client, message.channel)

    elif message.content.startswith(">misc help"):
        await helpCommands.miscHelp(client, message.channel)

    elif message.content.startswith(">misc playercount"):
        await miscCommands.miscPlayerCount(client, message.channel)

    elif message.content.startswith(">mc help"):
        await helpCommands.mcHelp(client, message.channel)

    elif message.content.startswith(">mc status"):
        await mcCommands.status(client, message.channel)
    
    elif message.content.startswith(">mc name"):
        # This gets everything after name
        args = " ".join(message.content.split(" ")[2:])
        await mcCommands.name(client, message.channel, args)
    
    elif message.content.startswith('>wiki help'):
        await helpCommands.wikiHelp(client, message.channel)
    
    elif message.content.startswith('>wiki locationlist'):
        await wikiCommands.locationlist(client,message.author)
    
    elif message.content.startswith('>wiki location'):
        args = " ".join(message.content.split(" ")[2:])
        await wikiCommands.location(client,message.channel, message.author, args)
    
    elif message.content.startswith('>wiki coord'):
        args = " ".join(message.content.split(" ")[2:])
        await wikiCommands.coords(client,message.channel,message.author,args)

    elif message.content.startswith('>wiki coord'):
        args = " ".join(message.content.split(" ")[2:])
        await wikiCommands.coords(client,message.channel,message.author,args)
    
    elif message.content.startswith('>wiki legendarylist'):
        args = " ".join(message.content.split(" ")[2:])
        await wikiCommands.legendarylist(client, message.channel, message.author, args)


keep_alive()
while(True):
    client.run(credentials.bot_token)
