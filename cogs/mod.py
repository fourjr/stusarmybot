import discord
from discord.ext import commands


class Mod():
    def __init__(self, bot):
        self.bot = bot

    def __local_check(self, ctx):
        return commands.has_any_role("SA1 | Leader", "SA2 | Leader", "SA3 | Leader", "SA4 | Leader", "SA5 | Leader", "SA6 | Leader")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        '''Kicks a member from the server.'''
        await member.kick(reason=reason)
        await ctx.send(f'{ctx.author.name} kicked {member.name}')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason=None):
        '''Use this on JJ :)'''
        await member.ban(reason=reason)
        await ctx.send(f'{ctx.author.name} banned {member.name}')


def setup(bot):
    bot.add_cog(Mod(bot))
