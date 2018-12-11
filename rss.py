import feedparser
import discord
import asyncio
from discord.ext import commands
import time
import pytz
from datetime import datetime
from datetime import timedelta

with open("config.cfg", "r") as configFile:
    config = configFile.readlines()

class RSSCog:
    def __init__(self,bot):
        
        self.bot = bot
        self.bot.enabled=True

    async def on_ready(self):

        async def start(self):
            start_time = time.gmtime()
            oldDate = None
            postingChannel = self.bot.get_channel(config[5][15:-1])
            rss_url="https://shotbow.net/forum/forums/-/index.rss"


            while self.bot.enabled==True:
                feed=feedparser.parse(rss_url)
                post = feed["items"][0]
                title = post.title
                url = post.link
                author = post.author
                date = post.published_parsed
                if date < start_time:
                    await asyncio.sleep(60)
                elif oldDate != date:
                    await self.bot.send_message(postingChannel, '```New Forum Post:\n' + title + '\nPostURL: ' + url + '\nAuthor:'+ author + '```')
                    oldDate = date
                    await asyncio.sleep(60)
                else:
                    await asyncio.sleep(60)

        self.bot.loop.create_task(start(self))
              

    @commands.group(pass_context=True,brief='\n    addchannel\n    removechannel')
    async def rss(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('`No valid command entered`')
            
    @rss.command(pass_context=True)
    async def help(self,ctx):
        embed = discord.Embed(title="RSS Commands", description="RSS Commands are:", color=0xeee657)

        embed.add_field(name=">rss addchannel", value="Adds current channel to recieve messages", inline=False)
        embed.add_field(name=">rss removechannel", value="Removes current channel from recieving messages", inline=False)
        await self.bot.send_message(ctx.message.channel, embed=embed)


        
def setup(bot):
    bot.add_cog(RSSCog(bot))

