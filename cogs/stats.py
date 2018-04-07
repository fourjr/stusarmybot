import asyncio
import copy

import clashroyale
import discord
from discord.ext import commands
from commands.cooldowns import BucketType

from .new_welcome import InvalidTag

class TagCheck(commands.Converter):
    check = 'PYLQGRJCUV0289'
    async def convert(self, ctx, argument):
        argument = argument.strip('#').upper().replace('O','0')
        if not any(i not in self.check for i in argument):
            return argument
        raise InvalidTag

class Stats:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def save(self, ctx, tag: TagCheck):
        '''Saves your game tag'''
        await self.bot.mongo.stusarmybot.player_tags.find_one_and_update({
            'user_id': ctx.author.id
        },
        {
            '$set':{
                'tag': tag
            }
        }, upsert=True)

        await ctx.send('Successfully saved tag.')

    @commands.has_any_role('leaders', 'Welcome Assistant')
    @commands.command()
    async def savefor(self, ctx, member: discord.Member, tag: TagCheck):
        '''Saves a tag for another user'''
        ctx.author = member
        await ctx.invoke(self.save, tag=tag)

    @commands.cooldown(1, 3600, BucketType.default)
    @commands.has_role('leaders')
    @commands.command()
    async def refresh(self, ctx):
        '''Refreshes all roles and ensures everyone has the right roles.'''
        tags = await self.bot.mongo.stusarmybot.player_tags.find().to_list(None)
        roles = copy.copy(self.bot.get_cog('Welcome').roles)
        del roles['visitor']
        role_ids = list(roles.values())

        await ctx.send('Tag checking has begun. Please note that this might take a long time to complete.')
        logs = ''

        for t in tags:
            try:
                profile = await self.bot.client.get_player(t['tag'])
            except (clashroyale.RequestError, clashroyale.NotResponding):
                logs += f'[API]: Paused for 2 seconds\n'
                await asyncio.sleep(2)

            member = ctx.guild.get_member(t['user_id'])

            if not member:
                continue

            clan_role = [r for r in member.roles if r.id in role_ids]

            member_role = discord.utils.get(ctx.guild.roles, name='member')
            try:
                sa_role = discord.utils.get(ctx.guild.roles, id=roles[profile.clan.tag])
            except (KeyError, AttributeError):
                # AttributeError is in case the user is not in any clan.
                # User is not in a SA Clan
                logs += f'[INFO] {member}: User not in an SA Clan\n'
                if clan_role:
                    # User has a SA Role
                    await member.remove_roles(*(clan_role + [member_role]))
                    logs += f'[REMOVE] {member} - {clan_role}: User not in an SA Clan\n'
            else:
                # User is in SA Clan
                logs += f'[INFO] {member}: User in SA Clan\n'
                if sa_role not in clan_role:
                    await member.add_roles(sa_role, member_role)
                    logs += f"[ADD] {member} - [{sa_role}]: User's SA Clan role was not given to user\n"

                if len(clan_role) > 1:
                    # Has 2 or more SA Roles
                    clan_role.remove(sa_role)
                    await asyncio.sleep(0.2)
                    await member.remove_roles(*clan_role)
                    logs += f"[REMOVE] {member} - {clan_role}: User has extra roles\n"

            logs += f'[INFO] {member}: User checked\n'
            await asyncio.sleep(0.4)

        async with self.bot.session.post('https://www.hastebin.com/documents', data=logs) as resp:
            data = await resp.json()

        await ctx.send(f'{ctx.author.mention}, we have finished the checking process. Please head to \
                         https://www.hastebin.com/{data["key"]} for the logs.')

    @commands.has_role('leaders')
    @commands.command()
    async def unsaved(self, ctx):
        '''Shows a list of users that have not saved their tags'''
        tags = [i['user_id'] for i in await self.bot.mongo.stusarmybot.player_tags.find().to_list(None)]
        paginator = commands.Paginator()
        roles = copy.copy(self.bot.get_cog('Welcome').roles)
        del roles['visitor']
        role_ids = list(roles.values())

        for i in ctx.guild.members:
            if i.id not in tags:
                if any([True if r.id in role_ids else False for r in i.roles]):
                    if '-mention' in ctx.message.content:
                        paginator.add_line(i.mention)
                    else:
                        paginator.add_line(str(i))

        for p in paginator.pages:
            await ctx.send(p)
        await ctx.send("That's all!")

def setup(bot):
    bot.add_cog(Stats(bot))
