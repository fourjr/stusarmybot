import discord
from discord.ext import commands
from PIL import Image
import os
import asyncio
import json
import aiohttp
import embedtobox
import io

class Commands:
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
    
    @commands.command(pass_context=True)
