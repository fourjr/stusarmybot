import discord
import clashroyale
import textwrap
from collections import OrderedDict
from discord.ext import commands
import re

class InvalidTag(commands.BadArgument):
    message = 'Player tags should only contain these characters:\n' \
              '**Numbers:** 0, 2, 8, 9\n' \
                '**Letters:** P, Y, L, Q, G, R, J, C, U, V'

class TagCheck(commands.MemberConverter):
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

        try:
            int(argument)
        except ValueError:
            if not any(i not in self.check for i in argument.strip('#').upper().replace('O','0')):
                return (argument, True)
            raise InvalidTag
        else:
            return (int(argument), False)

class Welcome:
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel = 385704172567265280
        self.keys = {
            'sa1':'88PYQV',
            'sa2':'29UQQ282',
            'sa3':'28JU8P0Y',
            'sa4':'8PUUGRYG'
        }
        self.roles = {
            '88PYQV':298816849968234496,
            '29UQQ282':298816905504882698,
            '28JU8P0Y':299912276008501248,
            '8PUUGRYG':329922314747641859,
            'visitor':298815975980138496
        }

    def __local_check(self, ctx):
        return ctx.channel.id == self.welcome_channel

    async def on_member_join(self, member):
        await self.bot.get_channel(self.welcome_channel).send('\n'.join((
            f"Hello there, {member.mention}! Welcome to the Stu's Army!\n",
            'If you are here to join us, please do the following commands:',
            '`>save YOUR_CR_TAG` (eg. `>save 2P0LYQ`)',
            '`>recommend`\n',
            'A list of clans you can join would pop up then. You may then join the clan and indicate you are from discord. After you get accepted, you can do the `>verify` command to get access to more channels.\n',
            f'User ID: {member.id}'))
        )

    @commands.command(aliases=['rec'])
    async def recommend(self, ctx, tag: TagCheck = None):
        '''Get clan recommendations!'''
        if tag is None:
            tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': ctx.author.id})
            if tag:
                tag = (tag['tag'], True)
            else:
                await ctx.send('Please save your tag using `>save PLAYER_TAG` first.')
                return

        try:
            sa = await self.bot.client.get_clan(*reversed(list(self.keys.values())))
            if tag[1] == True:
                trophies = (await self.bot.client.get_player(tag[0])).trophies  
            else:
                trophies = tag[0]
        except clashroyale.RequestError as e:
            return await ctx.send(e)

        suggest = 0

        for clan in sa:
            if trophies < clan.required_score:
                break
            suggest += 1
        # sa[suggest - 1] is the highest clan they can go to
        waiting = []
        waitinglist = (await ctx.guild.get_channel(431112508296790016).get_message(431113789161865241)).embeds[0].fields
        for item in waitinglist:
            val = int(item.value.splitlines()[0].strip('__').strip('Waiting: '))
            waiting.append(val)
        em = discord.Embed(title="Stu's Army!", description='We currently have 4 clans! These are the clans that you can go to. \nYour current trophies: ' + str(trophies), color=0xe67e22)
        fields = OrderedDict()

        for i in range(suggest):
            name = ''
            if waiting[i] != 0: 
                name += f'[WAITING: {waiting[i]}] '
            elif len(sa[i].members) == 50:
                name += '[FULL] '
            name += f'{sa[i].name} (#{sa[i].tag})'
            value = f':trophy: {sa[i].required_score} \n:medal: {sa[i].score} \n<:soon:337920093532979200> {sa[i].donations}/week'
            fields[name] = value

        for k in reversed(fields):
            em.add_field(name=k, value=fields[k], inline=False)

        if len(fields) == 0:
            em.add_field(name='Unsuitable', value='You currently have too little trophies to join any of our clans.')

        await ctx.send(embed=em)

    @commands.has_role('Welcome Assistant')
    @commands.command(name='waiting')
    async def _waiting(self, ctx, clan, *, member:discord.Member = None):
        member = member or ctx.author

        clan = clan.lower()
        if clan not in self.keys:
            return await ctx.send('Invalid clan.')

        claninfo = await self.bot.client.get_clan(self.keys[clan])
        if claninfo.member_count < 50:
            return await ctx.send("Clan isn't full, join the clan and then do `>verify`")

        tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': member.id})
        if tag:
            tag = tag['tag']
        else:
            return await ctx.send('Please save your tag using `>save PLAYER_TAG` first.')

        player = await self.bot.client.get_player(tag)
        if player.trophies < claninfo.required_score:
            return await ctx.send(f'Please hit the minimum required trophies ({claninfo.required_score}) first.')

        waiting_message = await ctx.guild.get_channel(431112508296790016).get_message(431113789161865241)
        waitinglist = OrderedDict(waiting_message.embeds[0].to_dict())
        for field in waitinglist['fields']:
            if str(ctx.author.id) in field['value']:
                return await ctx.send(f'{member.name} is already on the waitlist for {field["name"]}!')


        waitval = waitinglist['fields'][int(clan.strip('sa'))-1]['value'].splitlines()
        waitno = int(waitval[0].strip('__').strip('Waiting: ')) + 1
        waitval[0] = f'__Waiting: {waitno}__'
        waitval.append(f'{member.name} ({member.id})')
        waitinglist['fields'][int(clan.strip('sa'))-1]['value'] = '\n'.join(waitval)

        em = discord.Embed.from_data(waitinglist)
        await waiting_message.edit(embed=em)
        await ctx.send(f"{member.mention}, you are the number {waitno} in the queue.")

    @commands.command()
    async def unwait(self, ctx, member:discord.Member = None):
        if member is None: member = ctx.author

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
    async def verify(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        tag = await ctx.bot.mongo.stusarmybot.player_tags.find_one({'user_id': member.id})
        if tag:
            tag = tag['tag']
        else:
            await ctx.send('Please save the tag using `>save PLAYER_TAG` first.')
            return

        profile = await self.bot.client.get_player(tag)

        member_role = discord.utils.get(ctx.guild.roles, name='Member')
        try:
            role = discord.utils.get(ctx.guild.roles, id=self.roles[profile.clan.tag])
        except KeyError:
            await ctx.send('You are not in any of our clans. Please do `>rec` to find out which clan you should join')
        else:
            await member.add_roles(role, member_role)
            await ctx.send(f'{role} added.')
            await self.bot.get_channel(298812318903566337).send(f'Welcome {member.mention} to {role}!')

def setup(bot):
    bot.add_cog(Welcome(bot))