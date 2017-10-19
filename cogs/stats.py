import discord
import asyncio
from discord.ext import commands
import aiohttp
import json

class Stats():
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    @commands.command()
    async def save(self, ctx, tag:str):
        await self.bot.web(f"make stusarmybottags | {ctx.author.id} | {tag.replace('#', '').upper()}")
        await ctx.send('Added to database')

    @commands.command()
    async def profile(self, ctx, tag = None):
        emoji = self.bot.emoji
        if tag == None:
            await self.bot.web(f'read stusarmybottags | {ctx.author.id} |')
            tagmsg = await self.bot.wait_for('message', check=self.bot.check)
            tag = tagmsg.content

        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.cr-api.com/profile/{tag.replace('#', '').upper()}") as d:
                crprof = await d.json()

        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.cr-api.com/constants') as d:
                constants = await d.json()

        chests = ''
        index = crprof['chestCycle']['position'] % len(constants['chestCycle']['order'])
        chestindex = crprof['chestCycle']['position']

        for i in range(10):
            if chestindex == crprof['chestCycle']['superMagicalPos']:
                chests += emoji('chestsupermagical') + ' '
            elif chestindex == crprof['chestCycle']['legendaryPos']:
                chests += emoji('chestlegendary') + ' '
            elif chestindex == crprof['chestCycle']['epicPos']:
                chests += emoji('chestepic') + ' '
            else:
                chests += emoji('chest' + constants['chestCycle']['order'][index].lower()) + ' '
            index += 1
            chestindex += 1

        deck = ''
        for i in range(8):
            deck += f"{emoji(crprof['currentDeck'][i]['name'].lower().replace(' ', ''))}{crprof['currentDeck'][i]['level']} "

        index = crprof['chestCycle']['position'] % len(constants['chestCycle']['order'])
        smc = crprof['chestCycle']['superMagicalPos'] - crprof['chestCycle']['position']
        legendary = crprof['chestCycle']['legendaryPos'] - crprof['chestCycle']['position']
        epic = crprof['chestCycle']['epicPos'] - crprof['chestCycle']['position']

        profile = discord.Embed(title=f"{crprof['name']} ({crprof['tag']})", url=f'https://statsroyale.com/profile/{tag}')
        profile.add_field(name='Trophies', value=f"{crprof['trophies']}/{crprof['stats']['maxTrophies']} PB {emoji('trophy')}", inline=True)
        profile.add_field(name=f"Chests ({crprof['chestCycle']['position']} opened)", value=f"{chests} {smc}{emoji('chestsupermagical')} {legendary}{emoji('chestlegendary')} {epic}{emoji('chestepic')}")
        profile.add_field(name='Deck', value=deck)

        await ctx.send(embed=profile)

def setup(bot):
    bot.add_cog(Stats(bot))
