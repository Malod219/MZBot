# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext.commands import Bot
import platform
from datetime import datetime
from keep_alive import keep_alive

#Credentials, Tokens etc
import credentials

# Modify command prefix
bot = Bot(description="PiPy Bot", command_prefix=">", pm_help = False)

#Prints generic bot information to consol
@bot.event
async def on_ready():
        print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
        print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
        print('Invitation to bring this to the server {}:'.format(bot.user.name))
        print('https://discordapp.com/oauth2/authorize?bot_id={}&scope=bot&permissions=8'.format(bot.user.id))
        print("Start time:" + datetime.now().strftime("%Y-%m-%d %H:%M"))
        bot.day=datetime.now().strftime("%Y-%m-%d")                          #For file names
        print(bot.day)
        return await bot.change_presence(game=discord.Game(name='MineZ'))

        
bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
        embed = discord.Embed(title="Help commands", description="Help Commands are:", color=0xeee657)
        embed.add_field(name=">wiki help", value="Lists commands for wiki", inline=False)
        embed.add_field(name=">mc help", value="Lists commands for mc", inline=False)
        embed.add_field(name=">reddit help", value="Lists commands for reddit", inline=False)
        embed.add_field(name=">twitter help", value="Lists commands for twitter", inline=False)
        embed.add_field(name=">rss help", value="Lists commands for rss/Shotbow Forum commands", inline=False)
        embed.add_field(name=">info", value="More information on the bot.", inline=False)
        await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def info(ctx):
        embed = discord.Embed(title="General Information", description="General Information on ShotBot project.", color=0xeee657)
        embed.add_field(name="Who it is developed by:", value="ODST: https://distortionlayers.neocities.org/", inline=False)
        embed.add_field(name="How you can support development:", value="Send me BTC or ETH.\nBTC: 1qaLaxJ2hD2o7xPwg53v9yciu53dAoaP9\nETH: 0x404BF5D3fbAA5D83780765aa7Af2F4FE18E4fFAE", inline=False)
        embed.add_field(name="Am I paid for this?", value="No.", inline=False)
        embed.add_field(name="Can I develop this with you?", value="Yes! This Bot is Open Source!\nhttps://github.com/Malod219/MZBot", inline=False)
        embed.add_field(name="Bugs/problems", value="PM me on discord ODST#7648, Will be patched if it is a bug/problem.", inline=False)
        await bot.send_message(ctx.message.channel, embed=embed)
        
initial_extensions=["namemc",
                    "reddit",
                    "wiki",
                    "misc",
                    "rss",
                    "twitter"
        ]
channellist=[]


if __name__=='__main__':
        for extension in initial_extensions:
                bot.load_extension(extension)

keep_alive()
bot.run(credentials.bot_token)
