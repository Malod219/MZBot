import praw
import discord
import asyncio
from discord.ext import commands
import credentials
import time

with open("config.cfg", "r") as configFile:
    config = configFile.readlines()


class RedditCog:
    def __init__(self, bot):

        self.bot = bot
        self.bot.enabled = True

    async def on_ready(self):

        reddit = praw.Reddit(
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            user_agent=credentials.user_agent)

        start_time = time.time()
        subreddit = reddit.subreddit('minez')
        postingChannel = self.bot.get_channel(config[2][18:0])
        currentPost = ""
        while self.bot.enabled == True:
            posts = subreddit.new(limit=1)
            for post in posts:
                if post == currentPost:
                    await asyncio.sleep(60)
                elif post.created_utc > start_time and post.title != currentPost:
                    await self.bot.send_message(postingChannel, '```New Reddit Post in r/'+config[1][10:]+':\n' + post.title + '\nPostURL: ' + post.url + '```')
                    currentPost = post.title
                    await asyncio.sleep(60)

    @commands.group(
        pass_context=True, brief='\n    addchannel\n    removechannel')
    async def reddit(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('`No valid command entered`')

    @reddit.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title="Reddit Commands",
            description="Reddit Commands are:",
            color=0xeee657)

        embed.add_field(
            name=">reddit addchannel",
            value="Adds current channel to recieve messages",
            inline=False)
        embed.add_field(
            name=">reddit removechannel",
            value="Removes current channel from recieving messages",
            inline=False)
        await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(RedditCog(bot))
