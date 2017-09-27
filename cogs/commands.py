import discord
import random
import asyncio
from discord.ext import commands

class Commands:
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
    
    @commands.command(pass_context=True)
    async def visitor(self, ctx):
        '''Get the Visitor and Member Role!'''
        if ctx.message.channel.id != '298816198349553665' and ctx.message.channel.id != '362172188301852672': return
        await self.bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298815975980138496'))
        await self.bot.say('I have given {} the Visitor and Member Roles!'.format(ctx.message.author.name))
    
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
    @commands.has_role("Welcome Assistant") 
    async def sa1(self, ctx, member:discord.Member):
        '''Gives the SA1 role and Member role to the specified member'''
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298816849968234496'))
        await self.bot.say('Given the SA1 Roles!')
            
    @commands.command(pass_context=True, aliases=['SA2'])
    @commands.has_role("Welcome Assistant") 
    async def sa2(self, ctx, member:discord.Member):
        '''Gives the SA2 role and Member role to the specified member'''
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298816905504882698'))
        await self.bot.say('Given the SA2 Roles!')
            
    @commands.command(pass_context=True, aliases=['SA3'])
    @commands.has_role("Welcome Assistant") 
    async def sa3(self, ctx, member:discord.Member):
        '''Gives the SA3 role and Member role to the specified member'''
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='299912276008501248'))
        await self.bot.say('Given the SA3 Roles!')
   
    @commands.command(pass_context=True, aliases=['SA4'])
    @commands.has_role("Welcome Assistant") 
    async def sa4(self, ctx, member:discord.Member):
        '''Gives the SA4 role and Member role to the specified member'''
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='329922314747641859'))
        await self.bot.say('Given the SA4 Roles!')
        
def setup(bot):
    bot.add_cog(Commands(bot))
