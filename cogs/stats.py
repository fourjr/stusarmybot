import asyncio
import copy
import random

import clashroyale
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from .welcome import InvalidTag


class TagCheck(commands.Converter):
    check = 'PYLQGRJCUV0289'

    async def convert(self, ctx, argument):
        argument = argument.strip('#').upper().replace('O', '0')
        if not any(i not in self.check for i in argument):
            return argument
        raise InvalidTag


class TagOrUser(commands.MemberConverter):

    async def convert(self, ctx, argument):
        try:
            member = await super().convert(ctx, argument)
        except commands.BadArgument:
            return await TagCheck().convert(ctx, argument)
        else:
            tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': member.id})
            if tag is None:
                tag = await ctx.bot.statsy_mongo.player_tags.clashroyale.find_one({'user_id': member.id})
                if tag is None:
                    raise InvalidTag
                else:
                    del tag['_id']
                    tag['tag'] = tag['tag'][0]
                    await ctx.bot.mongo.stusarmybot.player_tags.insert_one(tag)
                    return tag['tag']
            else:
                return tag['tag']


class Stats:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def save(self, ctx, tag: TagCheck):
        """Saves your game tag"""
        await self.bot.mongo.stusarmybot.player_tags.find_one_and_update({
            'user_id': ctx.author.id
        },
            {
            '$set': {
                'tag': tag
            }
        }, upsert=True)

        await ctx.send('Successfully saved tag.')

    @commands.has_any_role('leaders', 'Welcome Assistant')
    @commands.command()
    async def savefor(self, ctx, member: discord.Member, tag: TagCheck):
        """Saves a tag for another user"""
        ctx.author = member
        await ctx.invoke(self.save, tag=tag)

    @commands.has_role('leaders')
    @commands.command()
    @commands.cooldown(1, 3600, BucketType.default)
    async def refresh(self, ctx):
        """Refreshes all roles and ensures everyone has the right roles."""
        tags = await self.bot.mongo.stusarmybot.player_tags.find().to_list(None)
        roles = copy.copy(self.bot.get_cog('Welcome').roles)
        keys = self.bot.get_cog('Welcome').keys
        del roles['visitor']
        role_ids = list(roles.values())

        await ctx.send('Tag checking has begun. Please note that this might take a long time to complete.')
        logs = ''

        for t in tags:
            while True:
                print(t)
                try:
                    profile = await self.bot.client.get_player(t['tag'])
                except clashroyale.NotFoundError:
                    break
                except (clashroyale.RequestError, clashroyale.NotResponding):
                    logs += f'[API]: Paused for 60 seconds\n'
                    await asyncio.sleep(60)
                else:
                    break

            member = ctx.guild.get_member(t['user_id'])

            if not member:
                continue

            clan_role = [r for r in member.roles if r.id in role_ids]

            member_role = discord.utils.get(ctx.guild.roles, name='member')
            try:
                sa_role = discord.utils.get(ctx.guild.roles, id=roles[profile.clan.tag])
                clan_key = next(x for x in keys if keys[x] == profile.clan.tag).upper()
            except (KeyError, AttributeError, StopIteration):
                # KeyError for role statement
                # AttributeError in case `profile.clan` is a NoneType
                # StopIteration for the next()
                logs += f'[INFO] {member}: User not in an SA Clan\n'
                if clan_role:
                    # User has a SA Role
                    await member.remove_roles(*(clan_role + [member_role]))
                    logs += f'[REMOVE] {member} - {clan_role}: User not in an SA Clan\n'

                    try:
                        # Nick cleanup checking
                        for k in keys:
                            if member.nick == f'{profile.name} | {k.upper()}':
                                raise StopIteration
                    except StopIteration:
                        try:
                            await member.edit(nick=None)
                        except discord.Forbidden:
                            logs += f'[NICK_REMOVE] [FORBIDDEN] {member} - {k.upper()}: User not in SA Clan'
                        else:
                            logs += f'[NICK_REMOVE] {member} - {k.upper()}: User not in SA Clan'
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

                # Check for nick
                if member.nick != f'{profile.name} | {clan_key}':
                    try:
                        await member.edit(nick=f'{profile.name} | {clan_key}')
                    except discord.Forbidden:
                        logs += f'[NICK_FORBIDDEN]'
                    else:
                        logs += f'[NICK_ADD]'
                    logs += f'{member} - {clan_key}: User does not have nickname\n'

            logs += f'[INFO] {member}: User checked\n'

        async with self.bot.session.post('http://mystb.in/documents', data=logs) as resp:
            data = await resp.json()

        await ctx.send(f'{ctx.author.mention}, we have finished the checking process. Please head to http://mystb.in/{data["key"]} for the logs.')

    @commands.has_role('leaders')
    @commands.command()
    async def unsaved(self, ctx):
        """Shows a list of users that have not saved their tags"""
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

    @commands.command()
    async def profile(self, ctx, *, tag_or_user: TagOrUser = None):
        """Displays basic CR Stats"""
        if tag_or_user is None:
            tag_or_user = await TagOrUser().convert(ctx, str(ctx.author.id))

        player = await self.bot.client.get_player(tag_or_user)

        em = discord.Embed(color=random.randint(0, 0xFFFFFF), timestamp=ctx.message.created_at)

        badge_image = self.bot.client.get_clan_image(player.clan)
        em.set_author(name=player.name, icon_url=badge_image)
        em.add_field(name='Trophies', value=f'{player.trophies} {self.bot.emoji("trophy")}')
        em.add_field(name='Level', value=f'{player.exp_level} {self.bot.emoji("experience")}')

        if player.clan:
            em.add_field(name='Clan Name', value=f'{player.clan.name} {self.bot.emoji("clan")}')
            em.add_field(name='Clan Tag', value=f'{player.clan.tag} {self.bot.emoji("clan")}')
            em.add_field(name='Clan Role', value=f'{player.role.title()} {self.bot.emoji("clan")}')
        else:
            em.add_field(name='Clan', value=f'Player not in clan {self.bot.emoji("clan")}')

        if player.stats.favorite_card:
            em.add_field(name='Favourite Card', value=self.bot.emoji(player.favorite_card.name))
        else:
            em.add_field(name='Favourite Card', value=f'No favourite card {self.bot.emoji("soon")}')

        em.add_field(name='Max Challenge Wins', value=f'{player.challenge_max_wins} {self.bot.emoji("tournament")}')

        deck = ''

        for c in player.current_deck:
            deck += f'{self.bot.emoji(c.name)} {c.level} '

        em.add_field(name='Battle Deck', value=deck, inline=False)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Stats(bot))
