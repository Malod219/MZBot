import tweepy
import discord
import asyncio
from discord.ext import commands
import credentials

auth = tweepy.OAuthHandler(credentials.consumer_key,
                           credentials.consumer_secret)
auth.set_access_token(credentials.access_token_key,
                      credentials.access_token_secret)

api=tweepy.API(auth)

class TwitterCog:
    def __init__(self,bot):
        
        self.bot = bot
        self.bot.enabled=True
        self.oldtweets=[]
        try:
            with open('PreviousTwitter.txt','r'):
                pass
        except:
            with open('PreviousTwitter.txt','w'):
                pass

    async def on_ready(self):
        while self.bot.enabled==True:
            alltweets = await tweetCheck(self)
            if alltweets!=self.oldtweets:
                
                for t in alltweets:
                    with open('PreviousTwitter.txt','r+') as r:
                        lines=r.read()
                        if t.full_text in lines:
                            same=True
                        else:
                            same=False
                    with open('TwitterChannelPosts.txt','r+') as r:
                        lines=r.readlines()
                        for line in lines:
                            line=line.replace('\n','')
                            channel=self.bot.get_channel(line)
                            try:
                                if same==False:
                                    if ('xpcode' in t.full_text.lower()):
                                        await self.bot.send_message(channel,'@everyone ```New Twitter Post from @ShotbowNetwork:\n'+t.full_text+'```')
                                    else:
                                        await self.bot.send_message(channel,'```New Twitter Post from @ShotbowNetwork:\n'+t.full_text+'```')
                            except:
                                pass
                    with open('PreviousTwitter.txt','w') as r:
                        r.write(t.full_text)

                self.oldtweets=alltweets
            await asyncio.sleep(300)

    
    @commands.group(pass_context=True,brief='\n    addchannel\n    removechannel')
    async def twitter(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('`No valid command entered`')
    @twitter.command(pass_context=True)
    async def help(self,ctx):
        embed = discord.Embed(title="Twitter Commands", description="Twitter Commands are:", color=0xeee657)

        embed.add_field(name=">twitter addchannel", value="Adds current channel to recieve messages", inline=False)
        embed.add_field(name=">twitter removechannel", value="Removes current channel from recieving messages", inline=False)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    @twitter.command(pass_context=True)
    async def addchannel(self,ctx):
        if ctx.message.author.server_permissions.administrator==True:
            channel=str(ctx.message.channel.id)
            try:
                with open('TwitterChannelPosts.txt','r+') as r:
                    pass
            except:
                with open('TwitterChannelPosts.txt','w+') as r:
                    pass
            with open('TwitterChannelPosts.txt','r+') as r:
                if channel in r.read():
                    print('FOUND!')
                else:
                    print('NOT FOUND, ADDING TO FILE')
                    r.write('\n'+channel)
            await self.bot.say('Added')
        else:
            await self.bot.say("You don't have Administrator permissions for this command")

    @twitter.command(pass_context=True)
    async def removechannel(self,ctx):
        if ctx.message.author.server_permissions.administrator==True:
            output=""
            channel=str(ctx.message.channel.id)

            with open('TwitterChannelPosts.txt','r+') as r:
                lines=r.readlines()
                print(lines)
                for line in lines:
                    if channel in line:
                        output+=""
                    else:
                        output+=(str(line)+'\n')
            with open('TwitterChannelPosts.txt','w+') as r:
                r.write(output)
                await self.bot.say('Removed')
        else:
            await self.bot.say("You don't have Administrator permissions for this command")

            
def setup(bot):
    bot.add_cog(TwitterCog(bot))

    
async def tweetCheck(self):
    tweets=api.user_timeline(screen_name="ShotbowNetwork",count=1,tweet_mode="extended")
    alltweets=[]
    alltweets.extend(tweets)
    return alltweets
