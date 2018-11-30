import feedparser
import discord
import asyncio
from discord.ext import commands


class RSSCog:
    def __init__(self,bot):
        
        self.bot = bot
        self.bot.enabled=True
        try:
            with open('PreviousRSS.txt','r'):
                pass
        except:
            with open('PreviousRSS.txt','w'):
                pass


    async def on_ready(self):
	
        oldTitle='123'
        title=''
        rss_url="https://shotbow.net/forum/forums/-/index.rss"
        while self.bot.enabled==True:
            feed=feedparser.parse(rss_url)
            post=feed["items"][0]
            title=post["title"]
            with open('PreviousRSS.txt','r+') as r:
                lines=r.readlines()
                if title in lines:
                    same=True
                else:
                    same=False
            url=post["link"]
            if (title!=oldTitle and same==False):
                with open('RSSChannelPosts.txt','r+') as r:
                    lines=r.readlines()
                for line in lines:
                    line=line.replace('\n','')
                    channel=self.bot.get_channel(line)
                    try:
                        await self.bot.send_message(channel,'```New Shotbow forum post:\n'+title+'\nPostURL: '+url+'\nAuthor: '+post["author"]+'```')
                    except:
                        pass
                with open('PreviousRSS.txt','w') as r:
                    r.write(title)
                oldTitle=title
            await asyncio.sleep(10)        

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


    @rss.command(pass_context=True)
    async def addchannel(self,ctx):
        if ctx.message.author.server_permissions.administrator==True:
            channel=str(ctx.message.channel.id)
            try:
                with open('RSSChannelPosts.txt','r+') as r:
                    pass
            except:
                with open('RSSChannelPosts.txt','w+') as r:
                    pass
            with open('RSSChannelPosts.txt','r+') as r:
                if channel in r.read():
                    print('FOUND!')
                else:
                    print('NOT FOUND, ADDING TO FILE')
                    r.write('\n'+channel)
            await self.bot.say('RSS channel added!')
        else:
            await self.bot.say("You don't have Administrator permissions for this command")

    @rss.command(pass_context=True)
    async def removechannel(self,ctx):
        if ctx.message.author.server_permissions.administrator==True:
            output=""
            channel=str(ctx.message.channel.id)

            with open('RSSChannelPosts.txt','r+') as r:
                lines=r.readlines()
                print(lines)
                for line in lines:
                    print(lines)
                    if channel in line:
                        output+=""
                    else:
                        output+=(str(line)+'\n')
                    print(output)
                    print('1')
            with open('RSSChannelPosts.txt','w+') as r:
                r.write(output)
                await self.bot.say('Removed')
        else:
            await self.bot.say("You don't have Administrator permissions for this command")


        
def setup(bot):
    bot.add_cog(RSSCog(bot))

