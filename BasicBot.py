# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import csv
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
from datetime import datetime

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
        return await bot.change_presence(game=discord.Game(name='MineZ'))#This is buggy, Works every now and then

        
bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
        embed = discord.Embed(title="Help commands", description="Help Commands are:", color=0xeee657)
        embed.add_field(name=">wiki help", value="Lists commands for wiki", inline=False)
        embed.add_field(name=">mc help", value="Lists commands for mc", inline=False)
        embed.add_field(name=">reddit help", value="Lists commands for reddit", inline=False)
        embed.add_field(name=">twitter help", value="Lists commands for twitter", inline=False)
        embed.add_field(name=">admin help", value="Lists commands for admin", inline=False)
        embed.add_field(name=">rss help", value="Lists commands for rss/Shotbow Forum commands", inline=False)
        embed.add_field(name=">info", value="More information on the bot.", inline=False)
        await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def info(ctx):
        embed = discord.Embed(title="General Information", description="General Information on ShotBot project.", color=0xeee657)
        embed.add_field(name="Who it is developed by:", value="Mr.Pi", inline=False)
        embed.add_field(name="How you can support development:", value="Share the bot invitation link N/A, or tip me money on my Patreon", inline=False)
        embed.add_field(name="Am I paid/volunteer developer for Shotbow?", value="No. I made this out of my own interest for computer Science."
                        "This means the quality of the bot will very likely be better than Shotbow standards.", inline=False)
        embed.add_field(name="Can I develop this with you?", value="Possibly. PM me on discord ODST#7648", inline=False)
        embed.add_field(name="Bugs/problems", value="PM me on discord ODST#7648, Will be patched if it is a bug/problem.", inline=False)
        await bot.send_message(ctx.message.channel, embed=embed)


#Chat Logs
@bot.event
async def on_message(message):
        author=message.author
        bot.author=author
        channel=message.channel
        bot.channel=channel
        server=message.server
        #Needed to prevent blocking of commands

        links=''
        try:
                attachments=message.attachments
                for item in attachments:
                        links=item['url']
        except:
                pass
        row=[str(server),str(channel),str(author),(str(message.content)+' '+links),datetime.now().strftime("%Y-%m-%d %H:%M")]
        if str(author.id)!="423953174911647765":
                with open("msglist.csv","a+") as hi:
                        writer=csv.writer(hi,lineterminator="\n")
                        writer.writerow(row)
        await bot.process_commands(message)

        
initial_extensions=[
        'Wiki',
        'Twitter',
        'Reddit',
        'Namemc',
        'Administration',
        'Misc',
        'RSS'
        ]
channellist=[]


if __name__=='__main__':
        for extension in initial_extensions:
                bot.load_extension(extension)
        
bot.run(credentials.bot_token)
