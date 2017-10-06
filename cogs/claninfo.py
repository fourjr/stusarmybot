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
    
    async def clanupdate(self, ctx):
        await self.bot.wait_until_ready()
        while not client.is_closed:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.cr-api.com/clan/88PYQV') as d:
                    sa1 = await d.json() 

            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.cr-api.com/clan/29UQQ282') as d:
                    sa2 = await d.json()

            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.cr-api.com/clan/28JU8P0Y') as d:
                    sa3 = await d.json()

            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.cr-api.com/clan/8PUUGRYG') as d:
                    sa4 = await d.json()

            message = '**SA1** \n:shield: {}/50 \n:trophy: {} \n:medal: {} \n--------------------- \n**SA2** \n:shield: {}/50 \n:trophy: {} \n:medal: {} \n--------------------- \n**SA3** \n:shield: {}/50 \n:trophy: {} \n:medal: {} \n--------------------- \n**SA4** \n:shield: {}/50 \n:trophy: {} \n:medal: {} \n---------------------'.format(sa1['memberCount'], sa1['requiredScore'], sa1['score'], sa2['memberCount'], sa2['requiredScore'], sa2['score'], sa3['memberCount'], sa3['requiredScore'], sa3['score'], sa4['memberCount'], sa4['requiredScore'], sa4['score'])
            await self.bot.edit_message(await self.bot.get_message(discord.utils.get(ctx.message.server.channels, id='365870449915330560'), '365888079665299457'), message)
            await asyncio.sleep(3600)
        
    self.bot.loop.create_task(clanupdate())
            
def setup(bot):
    bot.add_cog(claninfo(bot))
