import discord
from discord.ext import commands


class Mod:
    def __init__(self, bot):
        self.bot = bot

    def __local_check(self, ctx):
        return ctx.top_role > discord.utils.get(ctx.guild, name='Moderator')

    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason=None):
        """Kicks a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f'{ctx.author.name} kicked {member.name}')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason=None):
        """BANHAMMER!"""
        await member.ban(reason=reason)
        await ctx.send(f'{ctx.author.name} banned {member.name}')

def setup(bot):
    bot.add_cog(Mod(bot))
