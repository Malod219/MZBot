import discord
from discord.ext import commands
import aiohttp
import async_timeout
from bs4 import BeautifulSoup
import json

#bot Location CommandParent
class misc:
    def __init__(self,bot):
        self.bot = bot
    @commands.group(pass_context=True)
    async def misc(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('No command entered.')


    @misc.command(pass_context=True)
    async def help(self,ctx):
        embed = discord.Embed(title="Misc Commands", description="Misc Commands are:", color=0xeee657)

        embed.add_field(name=">misc playercount", value="Gives a list of servers and the number online", inline=False)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    @commands.cooldown(rate=1, per=300.0, type=commands.BucketType.user)
    @misc.command(pass_context=True)
    async def kittypost(self,ctx):
        async with aiohttp.ClientSession() as session:
            data=await fetch(session,"http://thecatapi.com/api/images/get?format=xml&results_per_page=1")
            soup=BeautifulSoup(data,"html.parser")
            lol=soup.findAll('url')[0].getText()
            await self.bot.say(lol)

    @kittypost.error
    async def lolnoped(self,ctx,error):
        await self.bot.say("Too much catnip... Try again in 5 minutes...")


    @misc.command(pass_context=True)
    async def playercount(self,ctx):
        async with aiohttp.ClientSession() as session:
            data=await fetch(session,'https://shotbow.net/serverList.json')
            d=json.loads(data)
            servs=""
            for key,value in d.items():
                try:
                    if int(value) < 1:
                        continue
                    if "us" in str(key) or "ddg" in str(key):
                        continue
                except:
                    pass
                servs+=(str(key).upper()+" has "+str(value)+" online\n")
            await self.bot.send_message(ctx.message.channel,("```"+servs+"```"))
                    
def setup(bot):
    bot.add_cog(misc(bot))


async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()
