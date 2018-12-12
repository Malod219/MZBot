from async_timeout import timeout
import dashtable
import aiohttp
from bs4 import BeautifulSoup
import discord

# This for functions that help other commands to keep them less bloated and more readable

# Fetch JSON stuff
async def fetch(session, url):
    async with timeout(10):
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
        async with aiohttp.ClientSession() as session:
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
                if templist!="":
                    leglist+='-'+templist
    except discord.errors.HTTPException:
        leglist=("Error requesting data from Shotbow...\nTry again....")
    return leglist