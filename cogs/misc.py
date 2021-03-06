import asyncio
import json
import os
import random

import aiohttp
import discord
from discord.ext import commands

class Misc:
    """Misc commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Get an invite to the server"""
        await ctx.send('https://discord.gg/hw9nmV2')

def setup(bot):
    bot.add_cog(Misc(bot))
