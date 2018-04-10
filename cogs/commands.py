import discord
import random
import json
import aiohttp
import asyncio
import os
from discord.ext import commands


class Misc:
    '''Misc commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def membercount(self, ctx):
        '''Outputs member count'''
        await ctx.send(f'Current member count: {len(ctx.guild.members)}')

    @commands.command()
    async def claninfo(self, ctx):
        message = await ctx.guild.get_channel(365870449915330560).get_message(371704816143040523)
        await ctx.send(embed = message.embeds[0])

    @commands.command()
    async def invite(self, ctx):
        await ctx.send('https://discord.gg/hw9nmV2')


def setup(bot):
    bot.add_cog(Commands(bot))
