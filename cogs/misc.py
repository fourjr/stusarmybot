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
    async def invite(self, ctx):
        await ctx.send('https://discord.gg/hw9nmV2')

def setup(bot):
    bot.add_cog(Misc(bot))
