import discord
from discord.ext import commands
import asyncio
import aiohttp

class Levelling():
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        
def setup(bot):
    bot.add_cog(Levelling(bot))