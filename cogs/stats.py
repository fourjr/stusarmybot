import asyncio
import copy
import random

import clashroyale
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from .new_welcome import InvalidTag


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
            tag = (await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': member.id}))['tag']
            if tag is None:
                raise InvalidTag
            else:
                return tag

def e(ctx, name):
    '''Converts anything to an emoji by it's name '''
    name = name.replace('.','').lower().replace(' ','').replace('_','').replace('-','')
    if name == 'chestmagic':
        name = 'chestmagical'
    return discord.utils.get(ctx.bot.emojis, name=name)

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
            '$set': {
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

    @commands.has_role('leaders')
    @commands.command()
    @commands.cooldown(1, 3600, BucketType.default)
    async def refresh(self, ctx):
        '''Refreshes all roles and ensures everyone has the right roles.'''
        tags = await self.bot.mongo.stusarmybot.player_tags.find().to_list(None)
        roles = copy.copy(self.bot.get_cog('Welcome').roles)
        keys = self.bot.get_cog('Welcome').keys
        del roles['visitor']
        role_ids = list(roles.values())

        await ctx.send('Tag checking has begun. Please note that this might take a long time to complete.')
        logs = ''

        for t in tags:
            try:
                profile = await self.bot.client.get_player(t['tag'])
            except (clashroyale.RequestError, clashroyale.NotResponding):
                logs += f'[API]: Paused for 60 seconds\n'
                await asyncio.sleep(60)

            member = ctx.guild.get_member(t['user_id'])

            if not member:
                continue

            clan_role = [r for r in member.roles if r.id in role_ids]

            member_role = discord.utils.get(ctx.guild.roles, name='member')
            try:
                sa_role = discord.utils.get(ctx.guild.roles, id=roles[profile.clan.tag])
                clan_key = next(x for x in keys if self.keys[x] == profile.clan.tag).upper()
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
                        await member.edit(nick=None)
                        logs += f'[NICK_REMOVE] {member} - {k.upper()}: User not in SA Clan'
            else:
                # User is in SA Clan
                logs += f'[INFO] {member}: User in SA Clan\n'
                nick_name = f''
                if member.nick != 
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
                if member.nick != f'{player.name} | {clan_key}':
                    await member.edit(nick=f'{player.name} | {clan_key}')
                    logs += logs += f'[NICK_ADD] {member} - {clan_key}: User does not have nickname'

            logs += f'[INFO] {member}: User checked\n'
            await asyncio.sleep(3)

        async with self.bot.session.post('https://www.hastebin.com/documents', data=logs) as resp:
            data = await resp.json()

        await ctx.send(f'{ctx.author.mention}, we have finished the checking process. Please head to https://www.hastebin.com/{data["key"]} for the logs.')

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

    @commands.command()
    async def profile(self, ctx, *, tag_or_user: TagOrUser = None):
        '''Displays basic CR Stats'''
        if tag_or_user is None:
            tag_or_user = await TagOrUser().convert(ctx, str(ctx.author.id))

        player = await self.bot.client.get_player(tag_or_user)

        em = discord.Embed(color=random.randint(0, 0xFFFFFF), timestamp=ctx.message.created_at)
        try:
            badge_image = player.clan.badge.image
        except AttributeError:
            badge_image = None
        em.set_author(name=player.name, icon_url=badge_image)
        em.add_field(name='Trophies', value=f'{player.trophies} {e(ctx, "trophy")}')
        em.add_field(name='Level', value=f'{player.stats.level} {e(ctx, "experience")}')

        if player.clan:
            em.add_field(name='Clan Name', value=f'{player.clan.name} {e(ctx, "clan")}')
            em.add_field(name='Clan Tag', value=f'{player.clan.tag} {e(ctx, "clan")}')
            em.add_field(name='Clan Role', value=f'{player.clan.role.title()} {e(ctx, "clan")}')
        else:
            em.add_field(name='Clan', value=f'Player not in clan {e(ctx, "clan")}')

        if player.stats.favorite_card:
            em.add_field(name='Favourite Card', value=e(ctx, player.stats.favorite_card.name))
        else:
            em.add_field(name='Favourite Card', value=f'No favourite card {e(ctx, "soon")}')

        em.add_field(name='Max Challenge Wins', value= f'{player.stats.challenge_max_wins} {e(ctx, "tournament")}')

        deck = ''

        for c in player.current_deck:
            deck += f'{e(ctx, c.name)} {c.level} '

        em.add_field(name='Battle Deck', value=deck, inline=False)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Stats(bot))
