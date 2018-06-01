import praw
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import credentials

reddit = praw.Reddit(
    client_id = credentials.client_id,
    client_secret = credentials.client_secret,
    password=credentials.password,
    user_agent=credentials.user_agent,
    username=credentials.username
    )

class RedditCog:
    def __init__(self,bot):
        
        self.bot = bot
        self.bot.enabled=True
        try:
            with open('PreviousReddit.txt','r'):
                pass
        except:
            with open('PreviousReddit.txt','w'):
                pass


    async def on_ready(self):
        oldTitle='123'
        title=''
        while self.bot.enabled==True:
            subreddit=reddit.subreddit('minez')
            posts=subreddit.new(limit=1)
            for post in posts:
                title=post.title
                with open('PreviousReddit.txt','r+') as r:
                    lines=r.readlines()
                    if title in lines:
                        same=True
                    else:
                        same=False
                url=post.url
            if (title!=oldTitle and same==False):
                with open('RedditChannelPosts.txt','r+') as r:
                    lines=r.readlines()
                for line in lines:
                    line=line.replace('\n','')
                    channel=self.bot.get_channel(line)
                    try:
                        await self.bot.send_message(channel,'```New Reddit Post in r/MineZ:\n'+title+'\nPostURL: '+url+'```')
                    except:
                        pass
                with open('PreviousReddit.txt','w') as r:
                    r.write(title)
                oldTitle=title
            await asyncio.sleep(10)        

    @commands.group(pass_context=True,brief='\n    addchannel\n    removechannel')
    async def reddit(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('`No valid command entered`')
            
    @reddit.command(pass_context=True)
    async def help(self,ctx):
        embed = discord.Embed(title="Reddit Commands", description="Reddit Commands are:", color=0xeee657)

        embed.add_field(name=">reddit addchannel", value="Adds current channel to recieve messages", inline=False)
        embed.add_field(name=">reddit removechannel", value="Removes current channel from recieving messages", inline=False)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    @reddit.command(pass_context=True)
    async def addchannel(self,ctx):
        if ctx.message.author.server_permissions.administrator==True:
            channel=str(ctx.message.channel.id)
            try:
                with open('RedditChannelPosts.txt','r+') as r:
                    pass
            except:
                with open('RedditChannelPosts.txt','w+') as r:
                    pass
            with open('RedditChannelPosts.txt','r+') as r:
                if channel in r.read():
                    print('FOUND!')
                else:
                    print('NOT FOUND, ADDING TO FILE')
                    r.write('\n'+channel)
            await self.bot.say('Reddit channel added!')
        else:
            await self.bot.say("You don't have Administrator permissions for this command")

    @reddit.command(pass_context=True)
    async def removechannel(self,ctx):
        if ctx.message.author.server_permissions.administrator==True:
            output=""
            channel=str(ctx.message.channel.id)

            with open('RedditChannelPosts.txt','r+') as r:
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
            with open('RedditChannelPosts.txt','w+') as r:
                r.write(output)
                await self.bot.say('Removed')
        else:
            await self.bot.say("You don't have Administrator permissions for this command")


        
def setup(bot):
    bot.add_cog(RedditCog(bot))

