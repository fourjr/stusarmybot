import discord
import asyncio
from discord.ext import commands
import aiohttp

class Stats():
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    def emoji(name:str):
        return discord.utils.get(bot.emojis, name=name)

    @commands.command()
    async def save(self, ctx, tag):
        await self.bot.web(f'make stusarmybottags | {ctx.author.id} | {tag.upper()}')
        await ctx.send('Added to database')

    @commands.command()
    async def profile(self, ctx, tag = None):
        if tag == None:
            await self.bot.web(f'read stusarmybottags | {ctx.author.id} |')
            tagmsg = await self.bot.wait_for('message', check=self.bot.check)
            tag = tagmsg.content

        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://api.cr-api.com/clan/{tag}') as d:
                crprof = await d.json()

        profile = discord.Embed(title=f'{crprof['name']}({crprof['tag']})', url=f'https://statsroyale.com/profile/{tag}')
        profile.add_field(name='Trophies', value=f'({crprof['trophies']} {emoji('trophy')}', inline=True)

def setup(bot):
    bot.add_cog(Stats(bot))
