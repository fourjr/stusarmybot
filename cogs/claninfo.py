import discord
from discord.ext import commands
from PIL import Image
import os
import asyncio
import io
import clashroyale
from datetime import datetime
from pytz import timezone


class claninfo():

    def __init__(self, bot):
        self.bot = bot
        self.sa_clans = ['88PYQV', '29UQQ282', '28JU8P0Y', '8PUUGRYG', '8YUU2CQV', '8VCGQL2C']
        self.clanupdateloopthing = self.bot.loop.create_task(self.clanupdateloop())

    def info(self, clan):
        # tier = 200
        # tiers = [70, 160, 270, 400, 550, 720, 910, 1120, 1350, 1600]
        # try:
        #     tier = tiers.index(max([n for n in tiers if (clan.clan_chest.crowns > n)])) + 2
        # except:
        #     tier = 0
        # if tier > 10: tier = 10

        return f''':shield: {clan.member_count}/50
:trophy: {clan.required_score}
:medal: {clan.score}
<:soon:337920093532979200> {clan.donations}/week'''
#:globe_with_meridians: {clan.type_name}'
#<:clanchest:366182009124421633> Tier {tier}

    async def clanupdate(self, message=None):
        sa = await self.bot.client.get_clans('88PYQV', '29UQQ282', '28JU8P0Y', '8PUUGRYG', '8YUU2CQV', '8VCGQL2C')

        embed = discord.Embed(title="Stu's Army!", color=0xf1c40f)
        embed.add_field(name='SA1', value=self.info(sa[0]))
        embed.add_field(name='SA2', value=self.info(sa[1]))
        embed.add_field(name='SA3', value=self.info(sa[2]))
        embed.add_field(name='SA4', value=self.info(sa[3]))
        embed.add_field(name='SA5', value=self.info(sa[4]))
        embed.add_field(name='SA6', value=self.info(sa[5]))
        total_members = sa[0].member_count + sa[1].member_count + sa[2].member_count + sa[3].member_count + sa[4].member_count + sa[5].member_count
        current_time = datetime.now(timezone('Europe/London')).strftime('%Y-%m-%d %H:%M:%S %p %Z')
        embed.add_field(name='More Info', value=f":busts_in_silhouette: {total_members}/300 \n \nLast updated {current_time}", inline=False)

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

    async def on_raw_reaction_add(self, emoji, message_id, channel_id, user_id):
        if message_id == 371704816143040523:
            member = self.bot.get_guild(298812318903566337).get_member(user_id)
            message = await self.bot.get_channel(365870449915330560).get_message(371704816143040523)
            if emoji.name != 'league7':
                return await message.remove_reaction(emoji, member)
            await self.clanupdate()
            await message.remove_reaction(emoji, member)


def setup(bot):
    bot.add_cog(claninfo(bot))
