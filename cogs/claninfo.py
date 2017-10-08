import discord
from discord.ext import commands
from PIL import Image
import os
import asyncio
import json
import aiohttp
import io

class claninfo():

    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        self.clanupdateloopthing = self.bot.loop.create_task(self.clanupdateloop())

    async def clanupdate(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/88PYQV') as d:
                sa1 = await d.json()
            async with session.get('http://api.cr-api.com/clan/29UQQ282') as d:
                sa2 = await d.json()
            async with session.get('http://api.cr-api.com/clan/28JU8P0Y') as d:
                sa3 = await d.json()
            async with session.get('http://api.cr-api.com/clan/8PUUGRYG') as d:
                sa4 = await d.json()
            async with session.get('http://api.cr-api.com/clan/8PUUGRYG') as d: #to add
                sa5 = await d.json()

        tiers = [70, 160, 270, 400, 550, 720, 910, 1120, 1350, 1600] 

        message = f'''**SA1** 
:shield: {sa1['memberCount']}/50 
:trophy: {sa1['requiredScore']} 
:medal: {sa1['score']} 
<:soon:337920093532979200> {sa1['donations']}/week
<:clanchest:366182009124421633> Tier {(tiers.index(max([n for n in tiers if (sa1['clanChest']['clanChestCrowns'] > n)])) + 2)} 
:globe_with_meridians: {sa1['typeName']} 
--------------------- 
**SA2** 
:shield: {sa2['memberCount']}/50 
:trophy: {sa2['requiredScore']}
:medal: {sa2['score']}
<:soon:337920093532979200> {sa2['donations']}/week
<:clanchest:366182009124421633> Tier {(tiers.index(max([n for n in tiers if (sa2['clanChest']['clanChestCrowns'] > n)])) + 2)} 
:globe_with_meridians: {sa2['typeName']} 
--------------------- 
**SA3** 
:shield: {sa3['memberCount']}/50 
:trophy: {sa3['requiredScore']} 
:medal: {sa3['score']} 
<:soon:337920093532979200> {sa3['donations']}/week
<:clanchest:366182009124421633> Tier {(tiers.index(max([n for n in tiers if (sa3['clanChest']['clanChestCrowns'] > n)])) + 2)} 
:globe_with_meridians: {sa3['typeName']} 
--------------------- 
**SA4** 
:shield: {sa4['memberCount']}/50 
:trophy: {sa4['requiredScore']} 
:medal: {sa4['score']} 
<:soon:337920093532979200> {sa4['donations']}/week
<:clanchest:366182009124421633> Tier {(tiers.index(max([n for n in tiers if (sa4['clanChest']['clanChestCrowns'] > n)])) + 2)} 
:globe_with_meridians: {sa4['typeName']} 
---------------------
**SA5**
Coming soon! :)
---------------------
:busts_in_silhouette: {(((int(sa1['memberCount']) + int(sa2['memberCount'])) + int(sa3['memberCount'])) + int(sa4['memberCount']))}/200'''

#:shield: {sa5['memberCount']}/50
#:trophy: {sa5['requiredScore']}
#:medal: {sa5['score']}
#<:soon:337920093532979200> {sa5['donations']}/week
#<:clanchest:366182009124421633> Tier {(tiers.index(max([n for n in tiers if (sa5['clanChest']['clanChestCrowns'] > n)])) + 2)}
#:globe_with_meridians: {sa5['typeName']}

        await (await discord.utils.get(discord.utils.get(self.bot.guilds, id=298812318903566337).channels, id=365870449915330560).get_message(365888079665299457)).edit(content=message)

    @commands.command(aliases=['SA1info', 'SA1-info', 'sa1-info'])
    async def sa1info(self, ctx):
        tag = '88PYQV'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/88PYQV') as d:
                data = await d.json()
        em = discord.Embed(color=discord.Color(value=3407664), title=f'''{data['name']} (#{tag})''', description=f'''{data['description']}''')
        em.set_author(name='Clan', url=f'''http://cr-api.com/clan/{tag}''', icon_url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.set_thumbnail(url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.add_field(name='Trophies', value=str(data['score']), inline=True)
        em.add_field(name='Type', value=data['typeName'], inline=True)
        em.add_field(name='Member Count', value=f'''{data['memberCount']}/50''', inline=True)
        em.add_field(name='Requirement', value=str(data['requiredScore']), inline=True)
        em.add_field(name='Donations', value=str(data['donations']), inline=True)
        em.add_field(name='Region', value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{data['members'][i]['name']}: {data['members'][i]['trophies']}
(#{data['members'][i]['tag']})''')
        em.add_field(name='Top 3 Players', value='\n\n'.join(players), inline=True)
        contributors = sorted(data['members'], key=(lambda x: x['clanChestCrowns']))
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}
(#{contributors[i]['tag']})''')
        em.add_field(name='Top CC Contributors', value='\n\n'.join(players), inline=True)
        em.set_footer(text='Powered by cr-api', icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
        await ctx.send(embed=em)

    @commands.command(aliases=['SA2info', 'SA2-info', 'sa2-info'])
    async def sa2info(self, ctx):
        tag = '29UQQ282'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/29UQQ282') as d:
                data = await d.json()
        em = discord.Embed(color=discord.Color(value=3407664), title=f'''{data['name']} (#{tag})''', description=f'''{data['description']}''')
        em.set_author(name='Clan', url=f'''http://cr-api.com/clan/{tag}''', icon_url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.set_thumbnail(url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.add_field(name='Trophies', value=str(data['score']), inline=True)
        em.add_field(name='Type', value=data['typeName'], inline=True)
        em.add_field(name='Member Count', value=f'''{data['memberCount']}/50''', inline=True)
        em.add_field(name='Requirement', value=str(data['requiredScore']), inline=True)
        em.add_field(name='Donations', value=str(data['donations']), inline=True)
        em.add_field(name='Region', value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{data['members'][i]['name']}: {data['members'][i]['trophies']}
(#{data['members'][i]['tag']})''')
        em.add_field(name='Top 3 Players', value='\n\n'.join(players), inline=True)
        contributors = sorted(data['members'], key=(lambda x: x['clanChestCrowns']))
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}
(#{contributors[i]['tag']})''')
        em.add_field(name='Top CC Contributors', value='\n\n'.join(players), inline=True)
        em.set_footer(text='Powered by cr-api', icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
        await ctx.send(embed=em)

    @commands.command(aliases=['SA3info', 'SA3-info', 'sa3-info'])
    async def sa3info(self, ctx):
        tag = '28JU8P0Y'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/28JU8P0Y') as d:
                data = await d.json()
        em = discord.Embed(color=discord.Color(value=3407664), title=f'''{data['name']} (#{tag})''', description=f'''{data['description']}''')
        em.set_author(name='Clan', url=f'''http://cr-api.com/clan/{tag}''', icon_url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.set_thumbnail(url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.add_field(name='Trophies', value=str(data['score']), inline=True)
        em.add_field(name='Type', value=data['typeName'], inline=True)
        em.add_field(name='Member Count', value=f'''{data['memberCount']}/50''', inline=True)
        em.add_field(name='Requirement', value=str(data['requiredScore']), inline=True)
        em.add_field(name='Donations', value=str(data['donations']), inline=True)
        em.add_field(name='Region', value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{data['members'][i]['name']}: {data['members'][i]['trophies']}
(#{data['members'][i]['tag']})''')
        em.add_field(name='Top 3 Players', value='\n\n'.join(players), inline=True)
        contributors = sorted(data['members'], key=(lambda x: x['clanChestCrowns']))
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}
(#{contributors[i]['tag']})''')
        em.add_field(name='Top CC Contributors', value='\n\n'.join(players), inline=True)
        em.set_footer(text='Powered by cr-api', icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
        await ctx.send(embed=em)

    @commands.command(aliases=['SA4info', 'SA4-info', 'sa4-info'])
    async def sa4info(self, ctx):
        tag = '8PUUGRYG'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/8PUUGRYG') as d:
                data = await d.json()
        em = discord.Embed(color=discord.Color(value=3407664), title=f'''{data['name']} (#{tag})''', description=f'''{data['description']}''')
        em.set_author(name='Clan', url=f'''http://cr-api.com/clan/{tag}''', icon_url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.set_thumbnail(url=f'''http://api.cr-api.com{data['badge']['url']}''')
        em.add_field(name='Trophies', value=str(data['score']), inline=True)
        em.add_field(name='Type', value=data['typeName'], inline=True)
        em.add_field(name='Member Count', value=f'''{data['memberCount']}/50''', inline=True)
        em.add_field(name='Requirement', value=str(data['requiredScore']), inline=True)
        em.add_field(name='Donations', value=str(data['donations']), inline=True)
        em.add_field(name='Region', value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{data['members'][i]['name']}: {data['members'][i]['trophies']}
(#{data['members'][i]['tag']})''')
        em.add_field(name='Top 3 Players', value='\n\n'.join(players), inline=True)
        contributors = sorted(data['members'], key=(lambda x: x['clanChestCrowns']))
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if (i <= 2):
                players.append(f'''{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}
(#{contributors[i]['tag']})''')
        em.add_field(name='Top CC Contributors', value='\n\n'.join(players), inline=True)
        em.set_footer(text='Powered by cr-api', icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
        await ctx.send(embed=em)

    @commands.command()
    async def update(self, ctx):
        await self.clanupdate()
        await ctx.message.add_reaction('league7:335746873753075714')

    async def clanupdateloop(self):
        await self.bot.wait_until_ready()
        while (not self.bot.is_closed):
            await self.clanupdate()
            await asyncio.sleep(3600)

    async def on_ready(self):
        await self.clanupdate()
        
def setup(bot):
    bot.add_cog(claninfo(bot))
