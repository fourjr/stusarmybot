import discord
from discord.ext import commands
from PIL import Image
import os
import asyncio
import json
import aiohttp
import io
from datetime import datetime
from pytz import timezone

class claninfo():

    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        self.clanupdateloopthing = self.bot.loop.create_task(self.clanupdateloop())

    def info(self, clan):
        tier = 200
        tiers = [70, 160, 270, 400, 550, 720, 910, 1120, 1350, 1600] 
        try:
            tier = tiers.index(max([n for n in tiers if (clan['clanChest']['clanChestCrowns'] > n)])) + 2
        except:
            tier = 0

        return f''':shield: {clan['memberCount']}/50 
:trophy: {clan['requiredScore']}
:medal: {clan['score']}
<:soon:337920093532979200> {clan['donations']}/week
<:clanchest:366182009124421633> Tier {tier} 
:globe_with_meridians: {clan['typeName']}'''

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
            async with session.get('http://api.cr-api.com/clan/8YUU2CQV') as d:
                sa5 = await d.json()

        embed = discord.Embed(title="Stu's Army!", color=0xf1c40f)
        embed.add_field(name='SA1', value=self.info(sa1))

        embed.add_field(name='SA2', value=self.info(sa2))
        embed.add_field(name='SA3', value=self.info(sa3))
        embed.add_field(name='SA4', value=self.info(sa4))
        embed.add_field(name='SA5', value=self.info(sa5))
        embed.add_field(name='More Info', value=f":busts_in_silhouette: {int(sa1['memberCount']) + int(sa2['memberCount']) + int(sa3['memberCount']) + int(sa4['memberCount']) + int(sa5['memberCount'])}/250 \n \nLast updated {datetime.now(timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M:%S')}")

        await (await discord.utils.get(discord.utils.get(self.bot.guilds, id=298812318903566337).channels, id=365870449915330560).get_message(371704816143040523)).edit(content='', embed=embed)

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

    @commands.command(aliases=['SA5info', 'SA45info', 'sa5-info'])
    async def sa5info(self, ctx):
        tag = '8YUU2CQV'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/8YUU2CQV') as d:
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
