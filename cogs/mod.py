import discord
from discord.ext import commands

class Mod():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def kick(self, ctx, member:discord.Member, reason=None):
        try:
            await member.kick(reason=reason)
        except:
            await ctx.send("I can't kick this user!")
        else:
            await ctx.send(f'{ctx.author.name} kicked {member.name}')

    @commands.command()
    async def ban(self, ctx, member:discord.Member, reason=None):
        try:
            await member.ban(reason=reason)
        except:
            await ctx.send("I can't kick this user!")
        else:
            await ctx.send(f'{ctx.author.name} kicked {member.name}')

def setup(bot):
    bot.add_cog(Mod(bot))