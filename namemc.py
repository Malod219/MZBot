import discord
from discord.ext import commands
import aiohttp
import async_timeout
import json

#bot Location CommandParent
class mc:
    def __init__(self,bot):
        self.bot = bot
    @commands.group(pass_context=True)
    async def mc(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('No command entered.')


    @mc.command(pass_context=True)
    async def help(self,ctx):
        embed = discord.Embed(title="Mc Commands", description="MC Commands are:", color=0xeee657)

        embed.add_field(name=">mc name [name]", value="Gives the past names of **name**", inline=False)
        embed.add_field(name=">mc status", value="Gives current minecraft server status", inline=False)
        await self.bot.send_message(ctx.message.channel, embed=embed)

                    
    @mc.command(pass_context=True)
    async def name(self,ctx,*args):
        name=" ".join(args)
        url='https://api.mojang.com/users/profiles/minecraft/'+name
        try:
            async with aiohttp.ClientSession() as session:
                data=await fetch(session,url)
                d=json.loads(data)
                ids=str(d['id'])
                url='https://api.mojang.com/user/profiles/'+ids+'/names'
                names=await fetch(session,url)
                names=list(reversed(json.loads(names)))
                
                output='Current name : `'+ name + '`\nPrevious names:\n'
                for counter, item in enumerate(names):
                    output+='`'+(names[counter]['name']+'`\n')
                await self.bot.say(output+'\nMore Info :` https://namemc.com/name/'+name+'`')
        except:
            await self.bot.say('No user exists with that name')

            
    @mc.command(pass_context=True)
    async def status(self,ctx):
        async with aiohttp.ClientSession() as session:
            data=await fetch(session,'https://status.mojang.com/check')
            d=json.loads(data)
            await self.bot.say('```Minecraft.net - '+str(d[0]["minecraft.net"])+
                               '\nAccounts Website - '+str(d[2]["account.mojang.com"])+
                               '\nAuthorization Service - '+str(d[3]["authserver.mojang.com"])+
                               '\nMultiplayer Session Service - '+str(d[4]["sessionserver.mojang.com"])+
                               '\nMinecraft Skins - '+str(d[6]["textures.minecraft.net"])+
                               '\nPublic API - '+str(d[5]["api.mojang.com"])+'```')
        
        
                    
def setup(bot):
    bot.add_cog(mc(bot))


async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()
