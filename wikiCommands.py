import discord
from discord.ext import commands
import aiohttp
import async_timeout
from bs4 import BeautifulSoup
import dashtable

import helperFunctions

async def locationlist(client, author):
    async with aiohttp.ClientSession() as session:
        locnamelist=[]
        output1=""
        output2=""
        html = await helperFunctions.fetch(session, 'https://shotbow.net/forum/wiki/minez-locations/')
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
        await client.send_message(author,output1)
        await client.send_message(author,output2)

#Coordinates
async def coords(client, channel, author, args):
    async with aiohttp.ClientSession() as session:
        name=args.replace(" ","-")
        name=name.lower()
        if name== (None or ""):
            await client.send_message(channel, 'You have to enter something dummy!')
        else:
            html = await helperFunctions.fetch(session, 'https://shotbow.net/forum/wiki/'+name)
            soup = BeautifulSoup(html,'html.parser')
            skip=False
            try:
                generalInfo = soup.find_all('table')[0]
                if 'Coordinates' in str(generalInfo):
                    pass
                else:
                    raise ValueError('Check')    
            except:
                await client.send_message(channel,"You didn't enter a valid location...")
                skip=True
            if skip!=True:
                links=generalInfo.find_all('a')
                for link in links:
                    if 'minez' in str(link):
                        url=link['href']
                        await client.send_message(channel,"Coordinates for "+name+" are at "+str(link.string)+'\nOn the MineZ Map: '+url)

async def legendarylist(client, channel, author, args):
    search=args.lower()
    person=author
    if search=='sword':
        leglist = await helperFunctions.getLegendary(0)
        await client.send_message(person,'```'+leglist+'```')
    elif search=='bow':
        leglist = await helperFunctions.getLegendary(1)
        await client.send_message(person,'```'+leglist+'```')
    elif ((search=='armour') or (search=='armor')):
        leglist = await helperFunctions.getLegendary(2)
        await client.send_message(person,'```'+leglist+'```')
    elif search=='misc':
        leglist = await helperFunctions.getLegendary(3)
        leglist1 = await helperFunctions.getLegendary(9)
        leglist2 = await helperFunctions.getLegendary(10)
        await client.send_message(person,'```'+leglist+'``````'+leglist1+'```')
        await client.send_message(person,'```'+leglist2+'```')
    elif search=='elite':
        leglist = await helperFunctions.getLegendary(4)
        leglist1 = await helperFunctions.getLegendary(5)
        leglist2 = await helperFunctions.getLegendary(6)
        leglist3 = await helperFunctions.getLegendary(7)
        leglist4 = await helperFunctions.getLegendary(8)
        await client.send_message(person,'```'+leglist+'``````'+leglist1+'```')
        await client.send_message(person,'```'+leglist2+'``````'+leglist3+'``````'+leglist4+'```')
    else:
        await client.send_message(channel, '`Invalid type. Valid types are: sword,bow,armour,misc,elite.`')

async def location(client, channel, author, args):
    try:
        async with aiohttp.ClientSession() as session:
            person=author
            print(person)
            name=args.replace(" ","-")
            name=name.lower()
            print(name)
            loclist=[]
            locnamelist=[]
            url = 'https://shotbow.net/forum/wiki/'+name
            html = await helperFunctions.fetch(session, url)
            loctype=""
            soup = BeautifulSoup(html,'html.parser')
            #Store all tables in HTML format to be parsed
            try:
                generalInfo = soup.find_all('table')[0]
            except:
                await client.send_message(channel, "You didn't enter a location...")
                url = 'https://fail'
                html = await helperFunctions.fetch(session, url)
                soup = BeautifulSoup(html,'html.parser')
                generalInfo = soup.find_all('table')[0]
            largeTable=soup.find_all('table')[1]#Table inside of a table. Necessary to parse through this table
            generalResources=largeTable.find_all('table')[0]
            
            if (("Dungeon" in str(generalInfo)) or ("Grand Library" in str(generalInfo))):
                loctype="dungeon"
                dungeonLoot=largeTable.find_all('table')[1]
                dungeonChests=largeTable.find_all('table')[2]
                if ("Axis Mundi" in str(dungeonChests)):
                    axisMundiKeys=largeTable.find_all('table')[2]
                    dungeonChests=largeTable.find_all('table')[3]
                    table2 = await helperFunctions.tableMakeExtend2(dungeonChests,axisMundiKeys)
                    table3 = await helperFunctions.tableMake(dungeonLoot)
                else:
                    table2 = await helperFunctions.tableMake(dungeonChests)
                    table3 = await helperFunctions.tableMake(dungeonLoot)
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
                    table4 = await helperFunctions.tableMake(spireLoot)
                        
                
                table2 = await helperFunctions.tableMakeExtend3(civilianLoot,foodLoot,roomLoot)
                table3 = await helperFunctions.tableMakeExtend3(potionLoot,toolLoot,milLoot)
            #Make table using tableMake function, takes input, cleans html and outputs a line by line table
            table0 = await helperFunctions.tableMake(generalInfo)
            table1 = await helperFunctions.tableMake(generalResources)
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
                await client.send_message(person,"General Information:\n`"+outputTable1+"`")
            else:
                await client.send_message(person,"Dungeon Info:\n`"+table0+"`")
                await client.send_message(person,"General Information:\n`"+table1+"`")
            await client.send_message(person,'Chest Loot:\n`'+outputTable+"`")
            if loctype=="spire":
                await client.send_message(person,'Spire Loot:\nm`'+table4+"`")
            await client.send_message(person,"More information found at:\n"+url+"\nMobile Users, Try tilting your phonhorizontally...")
    except discord.errors.HTTPException:
        await client.bot.send_message(channel, "Error requesting data from Shotbow...\nTry again....")