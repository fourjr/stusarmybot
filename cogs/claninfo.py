import discord
from discord.ext import commands
from PIL import Image
import os
import asyncio
import io
from datetime import datetime
from pytz import timezone
import crasync

class claninfo():

    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        self.clanupdateloopthing = self.bot.loop.create_task(self.clanupdateloop())

    def info(self, clan):
        tier = 200
        tiers = [70, 160, 270, 400, 550, 720, 910, 1120, 1350, 1600] 
        try:
            tier = tiers.index(max([n for n in tiers if (clan.clan_chest.crowns > n)])) + 2
        except:
            tier = 0
        if tier > 10: tier = 10

        return f''':shield: {len(clan.members)}/50 
:trophy: {clan.required_trophies}
:medal: {clan.score}
<:soon:337920093532979200> {clan.donations}/week
<:clanchest:366182009124421633> Tier {tier} 
:globe_with_meridians: {clan.type_name}'''

    async def clanupdate(self, message=None):
        try:
            sa = await self.bot.client.get_clan('88PYQV,29UQQ282,28JU8P0Y,8PUUGRYG,8YUU2CQV')
        except Exception as error:
            if message is not None:
                await message.add_reaction(self.bot.emoji('Lag', emojiresp=True))
                await message.channel.send(error)
            return

        embed = discord.Embed(title="Stu's Army!", color=0xf1c40f)
        embed.add_field(name='SA1', value=self.info(sa[0]))
        embed.add_field(name='SA2', value=self.info(sa[1]))
        embed.add_field(name='SA3', value=self.info(sa[2]))
        embed.add_field(name='SA4', value=self.info(sa[3]))
        embed.add_field(name='SA5', value=self.info(sa[4]))
        embed.add_field(name='More Info', value=f":busts_in_silhouette: {int(len(sa[0].members)) + int(len(sa[1].members)) + int(len(sa[2].members)) + int(len(sa[3].members)) + int(len(sa[4].members))}/250 \n \nLast updated {datetime.now(timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M:%S')}", inline=False)

        await (await self.bot.get_channel(365870449915330560).get_message(371704816143040523)).edit(content='', embed=embed)
        if message != None:
            await message.add_reaction(self.bot.emoji('league7', emojiresp=True))

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
