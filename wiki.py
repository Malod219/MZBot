import discord
from discord.ext import commands
import aiohttp
import async_timeout
from bs4 import BeautifulSoup
import dashtable

#bot Location CommandParent
class wiki:
    def __init__(self,bot):
        self.bot = bot
    @commands.group(pass_context=True)
    async def wiki(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('`No valid command entered`')

    @wiki.command(pass_context=True)
    async def help(self,ctx):
        embed = discord.Embed(title="Wiki Commands", description="Wiki Commands are:", color=0xeee657)

        embed.add_field(name=">wiki location [name]", value="Gives the general information of **name**", inline=False)
        embed.add_field(name=">wiki locationlist", value="Gives a list of all locations", inline=False)
        embed.add_field(name=">wiki legendary [name]", value="Gives information on **name**. Note it have proper grammar.", inline=False)
        embed.add_field(name=">wiki legendarylist [type]", value="List legendaries for **type**. Type can be sword,bow,armour,misc,elite.", inline=False)
        await self.bot.send_message(ctx.message.channel, embed=embed)

                    
    #Web Scrape the shotbow wiki location list, and compile into a neat alphabetic list
    @wiki.command(pass_context=True, aliases=['locationslist','listlocations','listloc'])
    async def locationlist(self,ctx,*args):
                async with aiohttp.ClientSession() as session:
                        person=ctx.message.author
                        locnamelist=[]
                        output1=""
                        output2=""
                        html = await fetch(session, 'https://shotbow.net/forum/wiki/minez-locations/')
                        topsnip,bottomsnip=html.split('<h2><a name="major-locations">')
                        c,d=bottomsnip.split('<h2><a name="removed-locations">')
                        html=c.encode()       
                        soup=BeautifulSoup(html,"html.parser")
                        for link in soup.find_all('a'):
                                locnamelist.append(link.text)
                        for counter, item in enumerate(locnamelist):
                                if len(output1)>1900:   #Discord character limit
                                        output2+=str(locnamelist[counter])
                                        output2+="  /  "
                                else:
                                        output1+=str(locnamelist[counter])
                                        output1+="  /  "
                                if counter==0:
                                        output1=""
                        await self.bot.send_message(person,output1)
                        await self.bot.send_message(person,output2)
                    
    #Coordinates
    @wiki.command(aliases=['coord'])
    async def coords(self,*args):
        async with aiohttp.ClientSession() as session:
            name=" ".join(args)
            name=name.replace(" ","-")
            name=name.lower()
            if name== (None or ""):
                await self.bot.say('You have to enter something dummy!')
            else:
                html = await fetch(session, 'https://shotbow.net/forum/wiki/'+name)
                soup = BeautifulSoup(html,'html.parser')
                skip=False
                try:
                    generalInfo = soup.find_all('table')[0]
                    if 'Coordinates' in str(generalInfo):
                        pass
                    else:
                        raise ValueError('Check')    
                except:
                    await self.bot.say("You didn't enter a valid location...")
                    skip=True
                if skip!=True:
                    links=generalInfo.find_all('a')
                    for link in links:
                        if 'minez' in str(link):
                            url=link['href']
                            print(url)
                            await self.bot.say("Coordinates for "+name+" are at "+str(link.string)+'\nOn the MineZ Map: '+url)


    @wiki.command(pass_context=True)
    async def legendarylist(self,ctx,*args):
        search=" ".join(args).lower()
        person=ctx.message.author
        if search=='sword':
            leglist = await getLegendary(0)
            await self.bot.send_message(person,'```'+leglist+'```')
        elif search=='bow':
            leglist = await getLegendary(1)
            await self.bot.send_message(person,'```'+leglist+'```')
        elif ((search=='armour') or (search=='armor')):
            leglist = await getLegendary(2)
            await self.bot.send_message(person,'```'+leglist+'```')
        elif search=='misc':
            leglist = await getLegendary(3)
            leglist1 = await getLegendary(9)
            leglist2 = await getLegendary(10)
            await self.bot.send_message(person,'```'+leglist+'``````'+leglist1+'```')
            await self.bot.send_message(person,'```'+leglist2+'```')
        elif search=='elite':
            leglist = await getLegendary(4)
            leglist1 = await getLegendary(5)
            leglist2 = await getLegendary(6)
            leglist3 = await getLegendary(7)
            leglist4 = await getLegendary(8)
            await self.bot.send_message(person,'```'+leglist+'``````'+leglist1+'```')
            await self.bot.send_message(person,'```'+leglist2+'``````'+leglist3+'``````'+leglist4+'```')
        else:
            await self.bot.say('`Invalid type. Valid types are: sword,bow,armour,misc,elite.`')

            
    @wiki.command()
    async def legendary(self,*args):
        search=" ".join(args).lower()
        try:
            with aiohttp.ClientSession() as session:
                    url = 'https://shotbow.net/forum/wiki/minez-legendary-items/'
                    html = await fetch(session, url)
                    soup = BeautifulSoup(html,'html.parser')
                    tables=soup.findChildren('table')
                    leglist=""
                    for table in tables:
                        rows = table.findChildren(['th','tr'])
                        for row in rows:
                            cells=row.findChildren('td')
                            templist=''
                            reallist=""
                            for cell in cells:
                                value=cell.string
                                if (value!=None and value!="\n"):
                                    templist+=value.lower()
                                    reallist+=value
                            if search in templist:
                                if templist!="":
                                    leglist+='-'+reallist
        except discord.errors.HTTPException:
            leglist=("Error requesting data from Shotbow...\nTry again....")
        if leglist=="":
            leglist="You didn't input a valid legendary!"
        await self.bot.say('`'+leglist+'`')

    #bot Wiki Parsing
    @wiki.command(pass_context=True)
    async def location(self,ctx,*args):
            try:
                    async with aiohttp.ClientSession() as session:
                            person=ctx.message.author
                            
                            print(person)
                            name=" ".join(args)
                            name=name.replace(" ","-")
                            name=name.lower()
                            loclist=[]
                            locnamelist=[]
                            url = 'https://shotbow.net/forum/wiki/'+name
                            html = await fetch(session, url)
                            loctype=""
                            soup = BeautifulSoup(html,'html.parser')
                            #Store all tables in HTML format to be parsed
                            try:
                                generalInfo = soup.find_all('table')[0]
                            except:
                                await self.bot.say("You didn't enter a location...")
                                url = 'https://fail'
                                html = await fetch(session, url)
                                soup = BeautifulSoup(html,'html.parser')
                                generalInfo = soup.find_all('table')[0]
                            largeTable=soup.find_all('table')[1]#Table inside of a table. Necessary to parse through this table
                            generalResources=largeTable.find_all('table')[0]

                            
                            if ("Dungeon" in str(generalInfo)) or("Grand Library" in str(generalInfo)):
                                    loctype="dungeon"
                                    dungeonLoot=largeTable.find_all('table')[1]
                                    dungeonChests=largeTable.find_all('table')[2]
                                    if ("Axis Mundi" in str(dungeonChests)):
                                        axisMundiKeys=largeTable.find_all('table')[2]
                                        dungeonChests=largeTable.find_all('table')[3]
                                        table2 = await tableMakeExtend2(dungeonChests,axisMundiKeys)
                                        table3 = await tableMake(dungeonLoot)
                                    else:
                                        table2 = await tableMake(dungeonChests)
                                        table3 = await tableMake(dungeonLoot)
                            else:
                                    loctype="other"
                                    civilianLoot=largeTable.find_all('table')[1]
                                    foodLoot=largeTable.find_all('table')[2]
                                    potionLoot=largeTable.find_all('table')[3]
                                    toolLoot=largeTable.find_all('table')[4]
                                    milLoot=largeTable.find_all('table')[5]
                                    roomLoot=largeTable.find_all('table')[6]
                                    if "Spire" in str(generalInfo):
                                        loctype="spire"
                                        spireLoot=largeTable.find_all('table')[7]
                                        table4 = await tableMake(spireLoot)
                                            
                                    
                                    table2 = await tableMakeExtend3(civilianLoot,foodLoot,roomLoot)
                                    table3 = await tableMakeExtend3(potionLoot,toolLoot,milLoot)
                            #Make table using tableMake function, takes input, cleans html and outputs a line by line table
                            table0 = await tableMake(generalInfo)
                            table1 = await tableMake(generalResources)
                            outputTable=""
                            outputTable1=""

                            if ("Dungeon" not in str(generalInfo)):
                                #Attaching multiple columns to final output
                                for counter,line0 in enumerate(table0.splitlines()):
                                        outputTable1+=line0+"\n"
                                        if line0=="":
                                                break
                                transform=outputTable1.splitlines()
                                for counter, line1 in enumerate(table1.splitlines()):
                                        if line1=="":
                                                break
                                        try:
                                                transform[counter]+='   '+line1+'\n'
                                        except:
                                                transform.append('                          '+line1+'\n')

                                outputTable1=' '+' '.join(transform)
                                outputTable1=outputTable1.replace("| +","|\n +")
                                outputTable1=outputTable1.replace("+ |","+\n |")
                                outputTable1=outputTable1.replace("+ +","+\n +")



                            
                            for counter, line2 in enumerate(table2.splitlines()):
                                    outputTable+=line2+"\n"
                                    if line2=="":
                                            break
                            transform=outputTable.splitlines()
                            for counter, line3 in enumerate(table3.splitlines()):
                                    if line3=="":
                                            break
                                    try:
                                            transform[counter]+='   '+line3+'\n'
                                    except:
                                            transform.append('                          '+line3+'\n')


                            outputTable=' '+' '.join(transform)
                            outputTable=outputTable.replace("| +","|\n +")
                            outputTable=outputTable.replace("+ |","+\n |")
                            outputTable=outputTable.replace("+ +","+\n +")
                            if outputTable1!="":
                                await self.bot.send_message(person,"General Information:\n`"+outputTable1+"`")
                            else:
                                await self.bot.send_message(person,"Dungeon Info:\n`"+table0+"`")
                                await self.bot.send_message(person,"General Information:\n`"+table1+"`")
                            await self.bot.send_message(person,'Chest Loot:\n`'+outputTable+"`")
                            if loctype=="spire":
                                await self.bot.send_message(person,'Spire Loot:\nm`'+table4+"`")
                            await self.bot.send_message(person,"More information found at:\n"+url+"\nMobile Users, Try tilting your phone horizontally...")
            except discord.errors.HTTPException:
                    await self.bot.say("Error requesting data from Shotbow...\nTry again....")
                    
def setup(bot):
    bot.add_cog(wiki(bot))

async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

        
async def tableMake(html1):
        html1 = await cleanHTML(html1)
        output = dashtable.html2rst(html1)
        return output


async def tableMakeExtend2(html1,html2):
        html1 = await cleanHTML(html1)
        html2 = await cleanHTML(html2)
        output = dashtable.html2rst(html1)+"\n"+dashtable.html2rst(html2)
        return output


async def tableMakeExtend3(html1,html2,html3):
        html1 = await cleanHTML(html1)
        html2 = await cleanHTML(html2)
        html3 = await cleanHTML(html3)
        output = dashtable.html2rst(html1)+"\n"+dashtable.html2rst(html2)+"\n"+dashtable.html2rst(html3)
        return output


async def cleanHTML(html):
        output=''
        anchors=html.findAll('a')
        for anchor in anchors:
                try:
                        if html!="generalInfo":
                                string=">>>"+anchor.string+"<<<"
                                anchor.string.replaceWith(string)
                except:
                        pass
                anchor.replaceWithChildren()
        html= str(html)
        k=html
        k=k.splitlines()
        for counter ,line in enumerate(k):
                line=line.replace('th colspan="3"','th colspan="2"')
                if 'img' in line:
                        line=''
                        k[counter+1]=''

                if line!='':
                        output+=line+'\n'
        return output
async def getLegendary(tableNo):
    try:
            with aiohttp.ClientSession() as session:
                    url = 'https://shotbow.net/forum/wiki/minez-legendary-items/'
                    html = await fetch(session, url)
                    soup = BeautifulSoup(html,'html.parser')
                    tables=soup.findChildren('table')
                    my_table=tables[tableNo]
                    rows = my_table.findChildren(['th','tr'])
                    leglist=""
                    for row in rows:
                        cells=row.findChildren('td')
                        templist=''
                        for cell in cells:
                            value=cell.string
                            if (value!=None and value!="\n"):
                                templist+=value
                        print(templist)
                        if templist!="":
                            leglist+='-'+templist
    except discord.errors.HTTPException:
            leglist=("Error requesting data from Shotbow...\nTry again....")
    return leglist
