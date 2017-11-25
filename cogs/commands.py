import discord
import random
import json
import aiohttp
import asyncio
from discord.ext import commands

class Commands():

    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    def welcomechannel(ctx):
        return (ctx.channel.id == 298816198349553665) or (ctx.channel.id == 362172188301852672)

    def anniversary(ctx):
        return False
    
    @commands.command()
    @commands.check(welcomechannel)
    async def visitor(self, ctx, member: discord.Member=None):
        'Get the Visitor Role!'
        if ((member == None) or (discord.utils.get(ctx.author.roles, id=334250664870019073) == None)):
            member = ctx.author
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=298815975980138496))
        await ctx.send('I have given {} the **Visitor** and **Member** Roles!'.format(member.name))
        await discord.utils.get(ctx.guild.channels, id=377204201408823296).send("Welcome {} to Stu's Army! He is a visitor!".format(member.mention))

    @commands.command(aliases=['SA1'])
    @commands.check(welcomechannel)
    async def sa1(self, ctx, member: discord.Member=None):
        'Gives the SA1 role and Member role to the specified member'
        if ((member == None) or (discord.utils.get(ctx.author.roles, id=334250664870019073) == None)):
            member = ctx.author
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=298817009372889088), discord.utils.get(ctx.guild.roles, id=298816849968234496))
        await ctx.send('I have given {} the **SA1** and **Member** Roles!'.format(member.name))
        await discord.utils.get(ctx.guild.channels, id=298812318903566337).send("Welcome {} to Stu's Army 1!".format(member.mention))

    @commands.command(aliases=['SA2'])
    @commands.check(welcomechannel)
    async def sa2(self, ctx, member: discord.Member=None):
        'Gives the SA2 role and Member role to the specified member'
        if ((member == None) or (discord.utils.get(ctx.author.roles, id=334250664870019073) == None)):
            member = ctx.author
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=298817009372889088), discord.utils.get(ctx.guild.roles, id=298816905504882698))
        await ctx.send('I have given {} the **SA2** and **Member** Roles!'.format(member.name))
        await discord.utils.get(ctx.guild.channels, id=298812318903566337).send("Welcome {} to Stu's Army 2!".format(member.mention))

    @commands.command(aliases=['SA3'])
    @commands.check(welcomechannel)
    async def sa3(self, ctx, member: discord.Member=None):
        'Gives the SA3 role and Member role to the specified member'
        if member == None or discord.utils.get(ctx.author.roles, id=334250664870019073) == None:
            member = ctx.author
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=298817009372889088), discord.utils.get(ctx.guild.roles, id=299912276008501248))
        await ctx.send('I have given {} the **SA3** and **Member** Roles!'.format(member.name))
        await discord.utils.get(ctx.guild.channels, id=298812318903566337).send("Welcome {} to Stu's Army 3!".format(member.mention))

    @commands.command(aliases=['SA4'])
    @commands.check(welcomechannel)
    async def sa4(self, ctx, member: discord.Member=None):
        'Gives the SA4 role and Member role to the specified member'
        if member == None or discord.utils.get(ctx.author.roles, id=334250664870019073) == None:
            member = ctx.author
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=298817009372889088), discord.utils.get(ctx.guild.roles, id=329922314747641859))
        await ctx.send('I have given {} the **SA4** and **Member** Roles!'.format(member.name))
        await discord.utils.get(ctx.guild.channels, id=298812318903566337).send("Welcome {} to Stu's Army 4!".format(member.mention))

    @commands.command(aliases=['SA5'])
    @commands.check(welcomechannel)
    async def sa5(self, ctx, member: discord.Member=None):
        'Gives the SA5 role and Member role to the specified member'
        if member == None or discord.utils.get(ctx.author.roles, id=334250664870019073) == None:
            member = ctx.author
        await member.add_roles(discord.utils.get(ctx.guild.roles, id=298817009372889088), discord.utils.get(ctx.guild.roles, id=366215438142537738))
        await ctx.send('I have given {} the **SA5** and **Member** Roles!'.format(member.name))
        await discord.utils.get(ctx.guild.channels, id=298812318903566337).send("Welcome {} to Stu's Army 5!".format(member.mention))

    @commands.command()
    async def membercount(self, ctx):
        '''Outputs member count'''
        await ctx.send(f'Current member count: {len(ctx.guild.members)}')

    @commands.command()
    @commands.check(anniversary)
    async def addrole(self, ctx, *, rolename:str):
        '''Adds some cool roles'''
        if rolename == '2 Year Crew':
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=368317195001921536))
            await ctx.send('Oh yeah! 2 Years! Welcome to the Crew!')
        elif rolename == '2 Year Tournament':
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=368317384148385792))
            await ctx.send('Welcome to the 2 Year Tournament! More details in <#368317815679221763>!')
        else:
            await ctx.send('Invalid Role!')

    @property
    def challonge(self):
        '''Returns your challonge token wherever it is'''
        try:
            with open('./data/config.json') as f:
                config = json.load(f)
                return config.get('CHALLONGE').strip('\"')
        except:
            return os.environ.get('CHALLONGE')
    
    @commands.check(lambda ctx: ctx.channel.id == 362172188301852672 or ctx.channel.id == 382967220499644416)
    @commands.command()
    async def scores(self, ctx, matchid:int, results:str):
        if results.split('-')[0] > results.split('-')[1]:
            winner = 'player1_id'
        else:
            winner = 'player2_id'
        async with self.bot.session.get('https://api.challonge.com/v1/tournaments/DecemberSA/matches.json', params={'api_key':self.challonge}) as resp:
            respj = await resp.json()
            if 300 > resp.status >= 200:
                print(json.dumps(await resp.json(), indent=4))
                async with self.bot.session.put('https://api.challonge.com/v1/tournaments/DecemberSA/matches/' + str(respj[matchid-1]['match']['id']) + f'.json', params={'api_key': self.challonge, 'match[scores_csv]': results, 'match[winner_id]': respj[matchid-1]['match'][winner]}) as resp2:
                    if 300 > resp2.status >= 200:
                        await message.add_reaction(self.bot.emoji('check', emojiresp=True))
                    else:
                        await message.add_reaction(self.bot.emoji('xmark', emojiresp=True))
                        try:
                            await self.bot.get_channel(362172188301852672).send('```py\n' + json.dumps(await resp2.json(), indent=4) + '\n```')
                        except:
                            print(json.dumps(await resp2.json(), indent=4))

            else:
                await message.add_reaction(self.bot.emoji('xmark', emojiresp=True))
                try:
                    await self.bot.get_channel(362172188301852672).send('```py\n' + json.dumps(respj, indent=4) + '\n```')
                except:
                    print(json.dumps(respj, indent=4))


    @commands.command() 
    async def claninfo(self, ctx):
        await ctx.send(embed=((await ctx.guild.get_channel(365870449915330560).get_message(371704816143040523)).embeds[0]))

def setup(bot):
    bot.add_cog(Commands(bot))
