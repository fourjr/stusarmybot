import asyncio
import io
import os
from datetime import datetime

import clashroyale
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from pytz import timezone

class ClanStats:
    """This cog handles #clan-stats, automatic updating of clan statistics"""
    def __init__(self, bot):
        self.bot = bot
        self.sa_clans = ['88PYQV', '29UQQ282', '28JU8P0Y', '8PUUGRYG']
        self.clan_update = self.bot.loop.create_task(self.clan_update_loop())

    def info(self, clan, war):
        return '\n'.join((f'<:clan:450920311832182786> {clan.member_count}/50',
                          f'<:trophy:451597507076554754> {clan.score}',
                          f'<:wartrophy:451595409295540226> {war.clan.war_trophies}',
                          f':medal: {clan.required_score} required',
                          f'<:cards:450917311692406784> {clan.donations}/week'
                        ))

    async def get_war(self, c):
        data = await self.bot.client.get_clan_war(c)
        await asyncio.sleep(0.5)
        return data

    async def clanupdate(self, message=None):
        sa = await self.bot.client.get_clans(*self.sa_clans)
        war = [await self.get_war(c) for c in self.sa_clans]

        embed = discord.Embed(title="Stu's Army!", color=0xf1c40f)
        for i in range(4):
            embed.add_field(name=f'SA{i+1}', value=self.info(sa[i], war[i]))
        total_members = sa[0].member_count + sa[1].member_count + sa[2].member_count + sa[3].member_count

        current_time = datetime.now(timezone('Europe/London')).strftime('%Y-%m-%d %H:%M:%S')
        embed.add_field(name='More Info', value=f":busts_in_silhouette: {total_members}/200 \n \nLast updated {current_time}", inline=False)

        await (await self.bot.get_channel(365870449915330560).get_message(477478236603809803)).edit(content='', embed=embed)
        if message:
            await message.add_reaction(self.bot.emoji('league7', emojiresp=True))

    @commands.command()
    @commands.cooldown(1, 10, BucketType.default)
    async def update(self, ctx):
        """Updates #clan-stats"""
        await self.clanupdate(ctx.message)

    async def clan_update_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            await self.clanupdate()
            await asyncio.sleep(14400)

    async def on_ready(self):
        await self.clanupdate()

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 477478236603809803:
            member = self.bot.get_guild(298812318903566337).get_member(payload.user_id)

            if member == self.bot.user:
                return

            message = await self.bot.get_channel(365870449915330560).get_message(477478236603809803)
            if payload.emoji.name == 'league7':
                await self.clanupdate()
            await message.clear_reactions()
            await message.add_reaction(discord.utils.get(self.bot.emojis, name='league7'))

def setup(bot):
    bot.add_cog(ClanStats(bot))
