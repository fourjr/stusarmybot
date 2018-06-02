import asyncio
import json
import random
import math

import discord
from discord.ext import commands
from pymongo import ReturnDocument

class Levelling:
    """Cog for levelling up while chatting"""
    def __init__(self, bot):
        self.bot = bot
        self.level_rewards = json.load(open('data/level_rewards.json'))
        self.level_ups = json.load(open('data/level_ups.json'))
        self.cooldown = []
        self.colors = self.colors = {'red':0xFF4500, 'green':0x00FF00, 'orange':0xFFC800, 'blue':0x5AADFF, 'pink':0xA4029B, 'light_red':0xFF1A1F}

    def calculate_level(self, xp):
        """Given an XP amount, return the level and the amount to get to the next level"""
        level = 3912
        count = math.inf
        for n, i in enumerate(self.level_ups):
            if i > xp:
                level = n
                count = i
                break
        return (level, count)

    async def on_message(self, msg):
        """Sets up the Levelling"""
        # Levels can only be earnt in #general
        if len(msg.content) > 5 and not msg.author.bot and msg.guild.id == 298812318903566337:
            if msg.author.id not in self.cooldown:
                self.cooldown.append(msg.author.id)
                entry = await self.bot.mongo.stusarmybot.levelling.find_one_and_update({'user_id':msg.author.id}, {'$inc':{'xp':random.randint(1, 5)}}, upsert=True, return_document=ReturnDocument.AFTER)
                amount = entry['xp']
                level = self.calculate_level(amount)[0]
                for i in self.level_rewards:
                    if level >= int(i):
                        role = discord.utils.get(msg.guild.roles, name=self.level_rewards[i])
                        if role not in msg.author.roles:
                            await msg.author.send(f'You just levelled up to level {level}!')
                            await msg.author.add_roles(role)
                await asyncio.sleep(random.randint(50, 150))
                self.cooldown.remove(msg.author.id)

    @commands.command()
    async def rank(self, ctx, member: discord.Member=None):
        """Check your current level!"""
        member = member or ctx.author
        entry = await self.bot.mongo.stusarmybot.levelling.find_one({'user_id':member.id})
        amount = 0 if entry is None else entry.get('xp')
        level = self.calculate_level(amount)
        em = discord.Embed(title='Rank!', color=self.colors['blue'])
        em.set_author(name=member.name, icon_url=member.avatar_url)
        em.add_field(name='XP', value=f'{amount}/{level[1]}')
        em.add_field(name='Level', value=level[0])
        await ctx.send(embed=em)
 
    @commands.command(aliases=['levellb', 'llb'])
    async def levels_leaderboard(self, ctx, page=1):
        """View how active you are compared to everyone else"""
        page -= 1
        top = await self.bot.mongo.stusarmybot.levelling.find().sort('xp', -1).to_list(None)
        sorted_top = sorted(top, key=lambda x: x.get('xp') or -9999999999, reverse=True)

        maxlen = 0
        for i in range(page*10, page*10 + 10):
            try:
                account = sorted_top[i]
            except IndexError:
                break
            user_name = getattr(self.bot.get_user(account['user_id']), 'name', False) or 'Left server'

            if len(f'{user_name}{account["xp"]}') > maxlen:
                maxlen = len(f'{user_name}{account["xp"]}') + 2

        fmt = ''

        for i in range(page*10, page*10 + 10):
            try:
                account = sorted_top[i]
            except IndexError:
                break
            user_name = getattr(self.bot.get_user(account['user_id']), 'name', False) or 'Left server'

            space_amt = maxlen - len(f'{user_name}{account["xp"]}')
            level = self.calculate_level(account['xp'])[0]
            fmt += f'{i+1}. {user_name} {" "*space_amt}{account["xp"]} (Level {level})\n'

        await ctx.send(f'```py\n{fmt}\n```')

    @commands.command()
    async def buy(self, ctx, item: str):
        """
        {
            "name": "a",
            "price": 80,
            "reward": {
                "name": "idk",
                "type": "role",
                "id": [],
                "id": 239294084378473
            }
        }
        """

        with open('data/level_shop.json') as f:
            shop_items = json.load(f)

        try:
            for i in shop_items:
                if item == i['name']:
                    wanted = i
                    raise StopIteration
            return await ctx.send('Invalid item.')

        except StopIteration:
            pass

        account = await self.bot.mongo.stusarmybot.levelling.find_one({'user_id': ctx.author.id})

        if account['xp'] < wanted['cost']:
            return await ctx.send('Not enough money.')

        if i['reward']['type'] == 'role':
            role_id = i['reward']['id']
            if isinstance(role_id, list):
                roles = []
                for r in role_id:
                    roles.append(discord.utils.get(ctx.guild.roles, id=r))
                await ctx.author.add_roles(*roles)

            else:
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=role_id))

        await ctx.send('Role awarded.')            



def setup(bot):
    bot.add_cog(Levelling(bot))
