import discord
import crasync
import textwrap
from collections import OrderedDict
from discord.ext import commands
import re

class InvalidTag(commands.BadArgument):
    message = 'Player tags should only contain these characters:\n' \
              '**Numbers:** 0, 2, 8, 9\n' \
                '**Letters:** P, Y, L, Q, G, R, J, C, U, V'

class TagCheck(commands.Converter):
    check = 'PYLQGRJCUV0289'
    async def convert(self, ctx, argument):
        argument = argument.strip('#').upper().replace('O','0')
        try:
            int(argument)
        except ValueError:
            if not any(i not in self.check for i in argument):
                return (argument, True)
            raise InvalidTag
        else:
            return (int(argument), False)

class Welcome():
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel = bot.get_channel(385704172567265280)
        self.keys = {'sa1':'88PYQV', 'sa2':'29UQQ282', 'sa3':'28JU8P0Y', 'sa4':'8PUUGRYG', 'sa5':'8YUU2CQV'}
        self.roles = {'88PYQV':298816849968234496, '29UQQ282':298816905504882698, '28JU8P0Y':299912276008501248, '8PUUGRYG':329922314747641859, '8YUU2CQV':366215438142537738, 'visitor':298815975980138496}
        
    async def on_member_join(self, member):
        await self.welcome_channel.send(textwrap.dedent('''
0. Hello there, {member.mention}! Welcome to the Stu's Army!
`_`
Please tell us if you are (pick one):
`1.` in our Clash Royale (CR) clans
`2.` interested in joining our CR clans
`3.` just visiting?
`_`
And provide one of the following:
`+` Player tag
`+` Screenshot of your profile
`_`
User ID: {member.id}'''))

    @commands.command(aliases=['rec'])
    async def recommend(self, ctx, tag: TagCheck):
        '''Get clan recommendations!'''
        try:
            sa = await self.bot.client.get_clan('8YUU2CQV,8PUUGRYG,28JU8P0Y,29UQQ282,88PYQV')
            if tag[1] == True:
                trophies = (await self.bot.client.get_profile(tag[0])).current_trophies
            else:
                trophies = tag[0]
        except Exception as e:
            return await ctx.send(e)
        suggest = 0
        for clan in sa:
            if trophies < clan.required_trophies:
                break
            suggest += 1
        # sa[suggest - 1] is the highest clan they can go to
        waiting = []
        waitinglist = (await ctx.guild.get_channel(385715575638196224).get_message(385723140933812224)).embeds[0].fields
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
            value = f':trophy: {sa[i].required_trophies} \n:medal: {sa[i].score} \n<:soon:337920093532979200> {sa[i].donations}/week'
            fields[name] = value
        for k in reversed(fields):
            em.add_field(name=k, value=fields[k], inline=False)
        if len(fields) == 0:
            em.add_field(name='Unsuitable', value='You currently have too little trophies to join any of our clans.')
        await ctx.send(embed=em)

    @commands.command(name='waiting')
    async def _waiting(self, ctx, clan, *, member:discord.Member = None):
        if member is None: member = ctx.author
        clan = clan.lower()
        if clan not in self.keys: return await ctx.send('Invalid clan.')

        claninfo = await self.bot.client.get_clan(self.keys[clan])
        if len(claninfo.members) < 50: return await ctx.send("Clan isn't full, use `>approve`!")

        waitinglist = OrderedDict((await ctx.guild.get_channel(385715575638196224).get_message(385723140933812224)).embeds[0].to_dict())
        for field in waitinglist['fields']:
            if ctx.author.id in field['value']:
                return await ctx.send(f'{member.name} is already on the waitlist for {field["name"]}!')
        waitval = waitinglist['fields'][int(clan.strip('sa'))-1]['value'].splitlines()
        waitno = int(waitval[0].strip('__').strip('Waiting: ')) + 1
        waitval[0] = f'__Waiting: {waitno}__'
        waitval.append(f'{member.name} ({member.id})')
        waitinglist['fields'][int(clan.strip('sa'))-1]['value'] = '\n'.join(waitval)

        em = discord.Embed.from_data(waitinglist)
        await (await ctx.guild.get_channel(385715575638196224).get_message(385723140933812224)).edit(embed=em)
        await ctx.send(f"{member.mention}, you are the number {waitno} in the queue.")

    @commands.command()
    async def unwait(self, ctx, member:discord.Member = None):
        if member is None: member = ctx.author
        
        waitinglist = OrderedDict((await ctx.guild.get_channel(385715575638196224).get_message(385723140933812224)).embeds[0].to_dict())
        for field in waitinglist['fields']:
            lines = field['value'].splitlines()
            linesold = lines
            lines = [x for x in lines if str(member.id) not in x]
            if lines != linesold:
                lines[0] = f"__Waiting: {int(lines[0].strip('__').strip('Waiting: ')) - 1}__"
                field['value'] = '\n'.join(lines)

        em = discord.Embed.from_data(waitinglist)
        await (await ctx.guild.get_channel(385715575638196224).get_message(385723140933812224)).edit(embed=em)
        await ctx.send(f'Cleared {ctx.author.name} from the waitlist.')

    @commands.command()
    async def register(self, ctx, tag, member:discord.Member):
        profile = await self.bot.client.get_profile(tag)
        if profile.clan_tag in self.roles:
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=self.roles[profile.clan_tag]))
        else:
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=self.roles['visitor']))

def setup(bot):
    bot.add_cog(Welcome(bot))