import discord
from discord.ext import commands
from PIL import Image
import os
import asyncio
import json
import aiohttp
import io

class claninfo:
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        self.clanupdateloopthing = self.bot.loop.create_task(self.clanupdateloop())

    async with aiohttp.ClientSession() as session:
        async with session.get('http://api.cr-api.com/clan/88PYQV') as d:
            sa1 = await d.json() 
        async with session.get('http://api.cr-api.com/clan/29UQQ282') as d:
            sa2 = await d.json()
        async with session.get('http://api.cr-api.com/clan/28JU8P0Y') as d:
            sa3 = await d.json()
        async with session.get('http://api.cr-api.com/clan/8PUUGRYG') as d:
            sa4 = await d.json()

    @commands.command(pass_context=True, aliases=['SA1info', 'SA1-info', 'sa1-info'])
    async def sa1info(self, ctx):
        tag = '88PYQV'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/88PYQV') as d:
                data = await d.json()  
                
        em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description=f"{data['description']}")
        em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
        em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
        em.add_field(name="Trophies", value=str(data['score']), inline=True)
        em.add_field(name="Type", value=data['typeName'], inline=True)
        em.add_field(name="Member Count", value=f"{data['memberCount']}/50", inline=True)
        em.add_field(name="Requirement", value=str(data['requiredScore']), inline=True)
        em.add_field(name="Donations", value=str(data['donations']), inline=True)
        em.add_field(name="Region", value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{data['members'][i]['name']}: {data['members'][i]['trophies']}\n(#{data['members'][i]['tag']})")
        em.add_field(name="Top 3 Players", value="\n\n".join(players), inline=True)
        contributors = sorted(data['members'], key=lambda x: x['clanChestCrowns'])
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}\n(#{contributors[i]['tag']})")
        em.add_field(name="Top CC Contributors", value='\n\n'.join(players), inline=True)
        em.set_footer(text="Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        await self.bot.say(embed=em)
        
    @commands.command(pass_context=True, aliases=['SA2info', 'SA2-info', 'sa2-info'])
    async def sa2info(self, ctx):
        tag = '29UQQ282'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/29UQQ282') as d:
                data = await d.json()  
                
        em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description=f"{data['description']}")
        em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
        em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
        em.add_field(name="Trophies", value=str(data['score']), inline=True)
        em.add_field(name="Type", value=data['typeName'], inline=True)
        em.add_field(name="Member Count", value=f"{data['memberCount']}/50", inline=True)
        em.add_field(name="Requirement", value=str(data['requiredScore']), inline=True)
        em.add_field(name="Donations", value=str(data['donations']), inline=True)
        em.add_field(name="Region", value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{data['members'][i]['name']}: {data['members'][i]['trophies']}\n(#{data['members'][i]['tag']})")
        em.add_field(name="Top 3 Players", value="\n\n".join(players), inline=True)
        contributors = sorted(data['members'], key=lambda x: x['clanChestCrowns'])
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}\n(#{contributors[i]['tag']})")
        em.add_field(name="Top CC Contributors", value='\n\n'.join(players), inline=True)
        em.set_footer(text="Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, aliases=['SA3info', 'SA3-info', 'sa3-info'])
    async def sa3info(self, ctx):
        tag = '28JU8P0Y'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/28JU8P0Y') as d:
                data = await d.json()  
                
        em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description=f"{data['description']}")
        em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
        em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
        em.add_field(name="Trophies", value=str(data['score']), inline=True)
        em.add_field(name="Type", value=data['typeName'], inline=True)
        em.add_field(name="Member Count", value=f"{data['memberCount']}/50", inline=True)
        em.add_field(name="Requirement", value=str(data['requiredScore']), inline=True)
        em.add_field(name="Donations", value=str(data['donations']), inline=True)
        em.add_field(name="Region", value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{data['members'][i]['name']}: {data['members'][i]['trophies']}\n(#{data['members'][i]['tag']})")
        em.add_field(name="Top 3 Players", value="\n\n".join(players), inline=True)
        contributors = sorted(data['members'], key=lambda x: x['clanChestCrowns'])
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}\n(#{contributors[i]['tag']})")
        em.add_field(name="Top CC Contributors", value='\n\n'.join(players), inline=True)
        em.set_footer(text="Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, aliases=['SA4info', 'SA4-info', 'sa4-info'])
    async def sa4info(self, ctx):
        tag - '8PUUGRYG'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/clan/8PUUGRYG') as d:
                data = await d.json()  
                
        em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description=f"{data['description']}")
        em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
        em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
        em.add_field(name="Trophies", value=str(data['score']), inline=True)
        em.add_field(name="Type", value=data['typeName'], inline=True)
        em.add_field(name="Member Count", value=f"{data['memberCount']}/50", inline=True)
        em.add_field(name="Requirement", value=str(data['requiredScore']), inline=True)
        em.add_field(name="Donations", value=str(data['donations']), inline=True)
        em.add_field(name="Region", value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{data['members'][i]['name']}: {data['members'][i]['trophies']}\n(#{data['members'][i]['tag']})")
        em.add_field(name="Top 3 Players", value="\n\n".join(players), inline=True)
        contributors = sorted(data['members'], key=lambda x: x['clanChestCrowns'])
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}\n(#{contributors[i]['tag']})")
        em.add_field(name="Top CC Contributors", value='\n\n'.join(players), inline=True)
        em.set_footer(text="Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        await self.bot.say(embed=em)

    async def self.clanupdate():
            tiers = [70, 160, 270, 400, 550, 720, 910, 1120, 1350, 1600]
            sa1cc = tiers.index(max([n for n in tiers if sa1['clanChest']['clanChestCrowns'] > n])) + 1
            sa2cc = tiers.index(max([n for n in tiers if sa2['clanChest']['clanChestCrowns'] > n])) + 1
            sa3cc = tiers.index(max([n for n in tiers if sa3['clanChest']['clanChestCrowns'] > n])) + 1
            sa4cc = tiers.index(max([n for n in tiers if sa4['clanChest']['clanChestCrowns'] > n])) + 1
            
        message = f'''**SA1** \n:shield: {sa1['memberCount']}/50 \n:trophy: {sa1['requiredScore']} \n:medal: {sa1['score']} \n<:clanchest:366182009124421633> Tier {sa1cc} \n:globe_with_meridians: {sa1['typeName']} \n--------------------- 
**SA2** \n:shield: {sa2['memberCount']}/50 \n:trophy: {sa2['requiredScore']} \n:medal: {sa2['score']} \n<:clanchest:366182009124421633> Tier {sa2cc} \n:globe_with_meridians: {sa2['typeName']} \n--------------------- 
**SA3** \n:shield: {sa3['memberCount']}/50 \n:trophy: {sa3['requiredScore']} \n:medal: {sa3['score']} \n<:clanchest:366182009124421633> Tier {sa3cc} \n:globe_with_meridians: {sa3['typeName']} \n--------------------- 
**SA4** \n:shield: {sa4['memberCount']}/50 \n:trophy: {sa4['requiredScore']} \n:medal: {sa4['score']} \n<:clanchest:366182009124421633> Tier {sa4cc} \n:globe_with_meridians: {sa4['typeName']} \n---------------------
:busts_in_silhouette: {int(sa1['memberCount']) + int(sa2['memberCount']) + int(sa3['memberCount']) + int(sa4['memberCount'])}/200'''
        await self.bot.edit_message(await self.bot.get_message(discord.utils.get(discord.utils.get(self.bot.servers, id='298812318903566337').channels, id='365870449915330560'), '365888079665299457'), message)
    
    async def self.clanupdateloop():
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            await self.clanupdate()
            await asyncio.sleep(3600)

    @commands.command(pass_context=True)
    async def update(ctx):
        await self.clanupdate()
        await self.bot.add_reaction(ctx.message, 'league7:335746873753075714')

    
def setup(bot):
    bot.add_cog(claninfo(bot))
