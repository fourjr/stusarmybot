import discord
import random
import asyncio
from discord.ext import commands

class Logging:
	def __init__(self, bot):
		self.bot = bot
        self.sessions = set()
    
    @commands.command(pass_context=True)
    async def trophy(self, ctx, trophy:int):
        '''We will suggest Clans that meet your trophy level!'''
        if trophy >= 3800:
            
