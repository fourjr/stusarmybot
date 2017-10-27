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
        if tier > 10: tier = 10

        return f''':shield: {clan['memberCount']}/50 
:trophy: {clan['requiredScore']}
:medal: {clan['score']}
<:soon:337920093532979200> {clan['donations']}/week
<:clanchest:366182009124421633> Tier {tier} 
:globe_with_meridians: {clan['typeName']}'''

    async def clanupdate(self, message = None):
        async with aiohttp.ClientSession() as session:
            sa = None
            async with session.get('http://api.cr-api.com/clan/88PYQV,29UQQ282,28JU8P0Y,8PUUGRYG,8YUU2CQV') as d:
                if d.status == 200: sa = await d.json()

            if sa == None:
                if message != None:
                    await message.add_reaction(self.bot.emoji('Lag', emojiresp=True))
                return
            try:
                temp = sa[0]['error']
            except:
                pass
            else:
                if message != None:
                    await ctx.send(sa[0]['error'])
                    await message.add_reaction(self.bot.emoji('Lag', emojiresp=True))
                return

        embed = discord.Embed(title="Stu's Army!", color=0xf1c40f)
        embed.add_field(name='SA1', value=self.info(sa[0]))
        embed.add_field(name='SA2', value=self.info(sa[1]))
        embed.add_field(name='SA3', value=self.info(sa[2]))
        embed.add_field(name='SA4', value=self.info(sa[3]))
        embed.add_field(name='SA5', value=self.info(sa[4]))
        embed.add_field(name='More Info', value=f":busts_in_silhouette: {int(sa[0]['memberCount']) + int(sa[1]['memberCount']) + int(sa[2]['memberCount']) + int(sa[3]['memberCount']) + int(sa[4]['memberCount'])}/250 \n \nLast updated {datetime.now(timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M:%S')}")

        await (await discord.utils.get(discord.utils.get(self.bot.guilds, id=298812318903566337).channels, id=365870449915330560).get_message(371704816143040523)).edit(content='', embed=embed)
        if message != None:
            await message.add_reaction(self.bot.emoji('league7', emoji=True))

    @commands.command()
    async def update(self, ctx):
        async with ctx.channel.typing():
            await self.clanupdate(ctx.message)

    async def clanupdateloop(self):
        await self.bot.wait_until_ready()
        while (not self.bot.is_closed):
            await self.clanupdate()
            await asyncio.sleep(3600)

    async def on_ready(self):
        await self.clanupdate()
        
def setup(bot):
    bot.add_cog(claninfo(bot))
