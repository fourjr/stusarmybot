import discord
import random
import asyncio
from discord.ext import commands
from ext import checks

class Logging:
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
    
    @commands.command(pass_context=True)
    async def visitor(self, ctx):
        '''Get the Visitor and Member Role!'''
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298815975980138496'))
    
    @commands.command(pass_context=True)
    async def trophy(self, ctx, trophy:int):
        '''We will suggest Clans that meet your trophy level!'''
        if ctx.message.channel.id != '298816198349553665' and ctx.message.channel.id != '362172188301852672': return
        if trophy >= 3800:
            await self.bot.say("You can check out Stu's Army 1! <@277389105501831170>, help him out!")
        elif trophy >= 2800:
            await self.bot.say("You can check out Stu's Army 2! <@277389105501831170>, help him out!")
        elif trophy >= 2400:
            await self.bot.say("You can check out Stu's Army 3! <@277389105501831170>, help him out!")
        elif trophy >= 2000:
            await self.bot.say("You can check out Stu's Army 2! <@277389105501831170>, help him out!")
        else:
            await self.bot.say("I'm sorry but you don't meet the criteria for any of our Clans. You can do `>visitor` if you want to stick around though!")

    @commands.command(pass_context=True, aliases=['SA1'])
    @checks.welcomeassistant()
    async def sa1(self, ctx, member:discord.Member):
        '''Gives the SA1 role and Member role to the specified Member'''
            await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298816849968234496'))
            await self.bot.say('Roles given!')
        
def setup(bot):
    bot.add_cog(Logging(bot))
