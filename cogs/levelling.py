import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
import json

class Levelling():
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    async def on_message(self, message):
        if message.author.bot == False and message.guild.id == 298812318903566337:
            data = []
            cooldown = False
            with open('./data/cooldown.json') as f:
                data = json.load(f)
            for item in data:
                if str(message.author.id) in item:
                    cooldown = data[item]
            if not cooldown and not message.author.bot:
                data.update({message.author.id: 'true'})
                with open('./data/cooldown.json', 'w') as f:
                    json.dump(data, f, indent=4)
                await self.bot.getdata2(f'xp {message.author.id}')
                await asyncio.sleep(5)
                del data[message.author.id]
                with open('./data/cooldown.json', 'w') as f:
                    json.dump(data, f, indent=4)

    @commands.command()
    async def rank(self, ctx, member:discord.Member = None):
        if member == None: member = ctx.author
        self.bot.tempvar = random.randint(1, 1000)
        await self.bot.getdata2(f'.xprank {ctx.author.id} | {self.bot.tempvar}')
        rank = await self.bot.wait_for('message', check=self.bot.checksplit)
        rankemb = discord.Embed(color=0x3498db)
        rankemb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        rankemb.add_field(name='XP', value=f"{int(rank.content.split()[1])}/{int(rank.content.split()[2])}")
        rankemb.add_field(name='Level', value=int(rank.content.split()[3]))
        await ctx.send(embed=rankemb)
        
def setup(bot):
    raise NotImplementedError('Logging cog not ready')
    bot.add_cog(Levelling(bot))