import asyncio
from collections import OrderedDict

import clashroyale
import discord
from discord.ext import commands


class InvalidTag(commands.BadArgument):
    message = 'Player tags should only contain these characters:\n' \
              '**Numbers:** 0, 2, 8, 9\n' \
              '**Letters:** P, Y, L, Q, G, R, J, C, U, V'


class TagCheck(commands.MemberConverter):
    """Code from Statsy"""
    check = 'PYLQGRJCUV0289'

    async def convert(self, ctx, argument):
        try:
            member = await super().convert(ctx, argument)
        except commands.BadArgument:
            pass
        else:
            tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': member.id})
            if tag:
                return (tag['tag'], True)
            tag = await ctx.bot.statsy_mongo.player_tags.clashroyale.find_one({'user_id': member.id})
            if tag:
                del tag['_id']
                tag['tag'] = tag['tag'][0]
                await ctx.bot.mongo.stusarmybot.player_tags.insert_one(tag)
                return (tag['tag'], True)

        try:
            int(argument)
        except ValueError:
            if not any(i not in self.check for i in argument.strip('#').upper().replace('O', '0')):
                return (argument, True)
            raise InvalidTag
        else:
            return (int(argument), False)


class Welcome:
    def __init__(self, bot):
        """Handles #welcome"""
        self.bot = bot
        self.welcome_channel = 385704172567265280
        self.keys = {
            'sa1': '88PYQV',
            'sa2': '29UQQ282',
            'sa3': '28JU8P0Y',
            'sa4': '8PUUGRYG'
        }
        self.roles = {
            '88PYQV': 298816849968234496,
            '29UQQ282': 298816905504882698,
            '28JU8P0Y': 299912276008501248,
            '8PUUGRYG': 329922314747641859,
            'visitor': 298815975980138496
        }

    def __local_check(self, ctx):
        return ctx.channel.id in (362172188301852672, self.welcome_channel)

    async def on_member_join(self, member):
        """Welcome message"""
        if member.guild.id == 298812318903566337:
            await self.bot.get_channel(self.welcome_channel).send(
                content=member.mention,
                embed=discord.Embed(
                    description='\n'.join((
                        f"Hello there, {member.name}! Welcome to the Stu's Army!\n",
                        'If you are here to join us, please do the following commands:',
                        '`>save YOUR_CR_TAG` (eg. `>save 2P0LYQ`)',
                        '`>recommend`\n',
                        'A list of clans you can join would pop up then. You may then join the clan and indicate you are from discord. After you get accepted, you can do the `>verify` command to get access to more channels.\n',
                        f'User ID: {member.id}'
                    )),

                    title="Stu's Army!",
                    color=0xf5f404
                )
            )
            await self.bot.get_channel(self.welcome_channel).send('<@&334250664870019073>', delete_after=0.2)

    async def on_member_remove(self, member):
        """Leave message"""
        await self.bot.get_channel(self.welcome_channel).send('{} has left us :('.format(member.name))

    async def get_clan(self, c):
        data = await self.bot.client.get_clan(c)
        await asyncio.sleep(0.02)
        return data

    @commands.command(aliases=['rec'])
    async def recommend(self, ctx, tag: TagCheck = None):
        """Get clan recommendations!"""
        if tag is None:
            tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': ctx.author.id})
            if tag:
                tag = (tag['tag'], True)
            else:
                await ctx.send('Please save your tag using `>save PLAYER_TAG` first.')
                return

        try:
            sa = [await self.get_clan(c) for c in reversed(list(self.keys.values()))]
            if tag[1]:
                trophies = (await self.bot.client.get_player(tag[0])).trophies
            else:
                trophies = tag[0]
        except clashroyale.RequestError as e:
            return await ctx.send(e)

        suggest = []

        for n, clan in enumerate(sa):
            if trophies < clan.required_trophies:
                continue
            suggest.append(n)
        # suggest is a list with indexes of clans they can go to
        waiting = []
        waitinglist = (await ctx.guild.get_channel(431112508296790016).get_message(431113789161865241)).embeds[0].fields
        for item in reversed(waitinglist):
            val = int(item.value.splitlines()[0].strip('__').strip('Waiting: '))
            waiting.append(val)
        em = discord.Embed(title="Stu's Army!", description='We currently have 4 clans! These are the clans that you can go to. \nYour current trophies: ' + str(trophies), color=0xe67e22)
        fields = OrderedDict()

        for i in suggest:
            name = ''
            if waiting[i] != 0:
                name += f'[WAITING: {waiting[i]}] '
            elif len(sa[i].member_list) == 50:
                name += '[FULL] '
            name += f'{sa[i].name} (#{sa[i].tag})'
            value = f':trophy: {sa[i].required_trophies} \n:medal: {sa[i].clan_score} \n<:soon:337920093532979200> {sa[i].donations_per_week}/week'
            fields[name] = value

        for k in reversed(fields):
            em.add_field(name=k, value=fields[k], inline=False)

        if len(fields) == 0:
            em.add_field(name='Unsuitable', value='You currently have too little trophies to join any of our clans.')

        await ctx.send(embed=em)

    @commands.has_role('Welcome Assistant')
    @commands.command(name='waiting')
    async def _waiting(self, ctx, clan, *, member: discord.Member):
        """Adds your name to the waiting list"""
        clan = clan.lower()
        if clan not in self.keys:
            return await ctx.send('Invalid clan.')

        claninfo = await self.bot.client.get_clan(self.keys[clan])
        if len(claninfo.member_list) < 50:
            return await ctx.send("Clan isn't full, join the clan and then do `>verify`")

        tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': member.id})
        if tag:
            tag = tag['tag']
        else:
            return await ctx.send('Please save your tag using `>save PLAYER_TAG` first.')

        player = await self.bot.client.get_player(tag)
        if player.trophies < claninfo.required_trophies:
            return await ctx.send(f'Please hit the minimum required trophies ({claninfo.required_trophies}) first.')

        waiting_message = await ctx.guild.get_channel(431112508296790016).get_message(431113789161865241)
        waitinglist = OrderedDict(waiting_message.embeds[0].to_dict())
        for field in waitinglist['fields']:
            if str(ctx.author.id) in field['value']:
                return await ctx.send(f'{member.name} is already on the waitlist for {field["name"]}!')

        waitval = waitinglist['fields'][int(clan.strip('sa')) - 1]['value'].splitlines()
        waitno = int(waitval[0].strip('__').strip('Waiting: ')) + 1
        waitval[0] = f'__Waiting: {waitno}__'
        waitval.append(f'{member.name} ({member.id})')
        waitinglist['fields'][int(clan.strip('sa')) - 1]['value'] = '\n'.join(waitval)

        em = discord.Embed.from_data(waitinglist)
        await waiting_message.edit(embed=em)
        await ctx.send(f"{member.mention}, you are the number {waitno} in the queue.")

    @commands.command()
    async def unwait(self, ctx, *, member: discord.Member = None):
        """Removes your name from the waiting list"""
        member = member or ctx.author

        waiting_message = await ctx.guild.get_channel(431112508296790016).get_message(431113789161865241)
        waitinglist = OrderedDict(waiting_message.embeds[0].to_dict())
        for field in waitinglist['fields']:
            lines = field['value'].splitlines()
            linesold = lines
            lines = [x for x in lines if str(member.id) not in x]
            if lines != linesold:
                lines[0] = f"__Waiting: {int(lines[0].strip('__').strip('Waiting: ')) - 1}__"
                field['value'] = '\n'.join(lines)

        em = discord.Embed.from_data(waitinglist)
        await waiting_message.edit(embed=em)
        await ctx.send(f'Cleared {ctx.author.name} from the waitlist.')

    @commands.command()
    async def verify(self, ctx, *, member: discord.Member = None):
        """Gives users appropriate roles"""
        member = member or ctx.author
        tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': member.id})
        if tag:
            tag = tag['tag']
        else:
            await ctx.send('Please save the tag using `>save PLAYER_TAG` first.')
            return

        profile = await self.bot.client.get_player(tag)

        member_role = discord.utils.get(ctx.guild.roles, name='member')
        try:
            role = discord.utils.get(ctx.guild.roles, id=self.roles[profile.clan.tag])
            clan_key = next(x for x in self.keys if self.keys[x] == profile.clan.tag).upper()
        except (KeyError, AttributeError, StopIteration):
            # KeyError for role statement
            # AttributeError in case `profile.clan` is a NoneType
            # StopIteration for the next()
            await ctx.send('You are not in any of our clans. Please do `>rec` to find out which clan you should join')
        else:
            await member.add_roles(role, member_role)
            await ctx.send(f'{role} added.')
            await member.edit(nick=f'{profile.name} | {clan_key}')
            await self.bot.get_channel(298812318903566337).send(f'Welcome {member.mention} to {role}!')

    @commands.command()
    async def visitor(self, ctx, member: discord.Member=None):
        """Get the Visitor Role!"""
        if member is None or ctx.author.top_role < discord.utils.get(ctx.guild.roles, id=334250664870019073):
            # Only welcome assistants or higher can tag
            member = ctx.author
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=298815975980138496))
        await ctx.send('I have given {} the **Visitor** role!'.format(member.name))
        await self.bot.get_channel(377204201408823296).send("Welcome {} to Stu's Army! He is a visitor!".format(member.mention))


def setup(bot):
    bot.add_cog(Welcome(bot))
