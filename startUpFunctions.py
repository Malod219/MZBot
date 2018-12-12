import time
import discord
import feedparser
import asyncio
import praw

import credentials

# RSS Watcher
async def rssWatch(client):
    start_time = time.gmtime()
    oldDate = None
    postingChannel = discord.Object(id='518109463446683652')
    rss_url="https://shotbow.net/forum/forums/-/index.rss"
    await client.send_message(postingChannel, '```RSS Operational```')

    while True:
        feed=feedparser.parse(rss_url)
        post = feed["items"][0]
        title = post.title
        url = post.link
        author = post.author
        date = post.published_parsed
        if date < start_time:
            await asyncio.sleep(60)
        elif oldDate != date:
            await client.send_message(postingChannel, '```New Forum Post:\n' + title + '\nPostURL: ' + url + '\nAuthor:'+ author + '```')
            oldDate = date
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(60)

# Subreddit Watcher
async def redditWatch(client, config):
    reddit = praw.Reddit(
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        user_agent=credentials.user_agent)
            
    start_time = time.time()
    subreddit = reddit.subreddit(config[1][10:-1])
    postingChannel = client.get_channel(config[2][18:-1])
    await client.send_message(postingChannel, '```Reddit Operational```')
    currentPost = ""
    while True:
        posts = subreddit.new(limit=1)
        for post in posts:
            if post == currentPost:
                await asyncio.sleep(60)
            elif post.created_utc > start_time and post.title != currentPost:
                await client.send_message(postingChannel, '```New Reddit Post in r/'+config[1][10:-1]+':\n' + post.title + '\nPostURL: ' + post.url + '```')
                currentPost = post.title
            await asyncio.sleep(60)

# HELP COMMANDS
async def help(client, channel):
        embed = discord.Embed(title="Help commands", description="Help Commands are:", color=0xeee657)
        embed.add_field(name=">wiki help", value="Lists commands for wiki", inline=False)
        embed.add_field(name=">mc help", value="Lists commands for mc", inline=False)
        embed.add_field(name=">reddit help", value="Lists commands for reddit", inline=False)
        embed.add_field(name=">twitter help", value="Lists commands for twitter", inline=False)
        embed.add_field(name=">rss help", value="Lists commands for rss/Shotbow Forum commands", inline=False)
        embed.add_field(name=">info", value="More information on the bot.", inline=False)
        await client.send_message(channel, embed=embed)

async def info(client, channel):
        embed = discord.Embed(title="General Information", description="General Information on ShotBot project.", color=0xeee657)
        embed.add_field(name="Who it is developed by:", value="ODST: https://distortionlayers.neocities.org/", inline=False)
        embed.add_field(name="How you can support development:", value="Send me BTC or ETH.\nBTC: 1qaLaxJ2hD2o7xPwg53v9yciu53dAoaP9\nETH: 0x404BF5D3fbAA5D83780765aa7Af2F4FE18E4fFAE", inline=False)
        embed.add_field(name="Am I paid for this?", value="No.", inline=False)
        embed.add_field(name="Can I develop this with you?", value="Yes! This Bot is Open Source!\nhttps://github.com/Malod219/MZBot", inline=False)
        embed.add_field(name="Bugs/problems", value="PM me on discord ODST#7648, Will be patched if it is a bug/problem.", inline=False)
        await client.send_message(channel, embed=embed)

async def miscHelp(client, channel):
        embed = discord.Embed(title="Misc Commands", description="Misc Commands are:", color=0xeee657)
        embed.add_field(name=">misc playercount", value="Gives a list of servers and the number online", inline=False)
        await client.send_message(channel, embed=embed)

async def mcHelp(client, channel):
    embed = discord.Embed(title="Mc Commands", description="MC Commands are:", color=0xeee657)

    embed.add_field(name=">mc name [name]", value="Gives the past names of **name**", inline=False)
    embed.add_field(name=">mc status", value="Gives current minecraft server status", inline=False)
    await client.send_message(channel, embed=embed)
