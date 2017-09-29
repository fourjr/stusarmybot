import discord
import random
import asyncio
from discord.ext import commands

class Commands:
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
    
    def welcomechannel(ctx):
        return ctx.message.channel.id == '298816198349553665' or ctx.message.channel.id == '362172188301852672'
    
    @commands.command(pass_context=True)
    @commands.check(welcomechannel)
    async def trophy(self, ctx, trophy:int):
        '''We will suggest Clans that meet your trophy level!'''
        if trophy >= 4000:
            await self.bot.say("You can check out Stu's Army 1! <@277389105501831170>, help him out!")
        elif trophy >= 2800:
            await self.bot.say("You can check out Stu's Army 2! <@277389105501831170>, help him out!")
        elif trophy >= 2400:
            await self.bot.say("You can check out Stu's Army 3! <@277389105501831170>, help him out!")
        elif trophy >= 2000:
            await self.bot.say("You can check out Stu's Army 2! <@277389105501831170>, help him out!")
        else:
            await self.bot.say("I'm sorry but you don't meet the criteria for any of our Clans. You can do `>visitor` if you want to stick around though!")
    
    @commands.command(pass_context=True)
    @commands.check(welcomechannel)
    async def visitor(self, ctx, member:discord.Member = None):
        '''Get the Visitor and Member Role!'''
        if member == None or discord.utils.get(ctx.message.author.roles, id='334250664870019073') == None:
            member = ctx.message.author
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298815975980138496'))
        await self.bot.say("I have given {} the **Visitor** and **Member** Roles!".format(member.name))

    @commands.command(pass_context=True, aliases=['SA1'])
    @commands.check(welcomechannel)
    async def sa1(self, ctx, member:discord.Member = None):
        '''Gives the SA1 role and Member role to the specified member'''
        if member == None or discord.utils.get(ctx.message.author.roles, id='334250664870019073') == None:
            member = ctx.message.author
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298816849968234496'))
        await self.bot.say("I have given {} the **SA1** and **Member** Roles!".format(member.name))
        await self.bot.send_message(discord.utils.get(ctx.message.server.channels, id='298812318903566337'), "Welcome {} to Stu's Army! He is a visitor!".format(ctx.message.author.mention))
            
    @commands.command(pass_context=True, aliases=['SA2'])
    @commands.check(welcomechannel)
    async def sa2(self, ctx, member:discord.Member = None):
        '''Gives the SA2 role and Member role to the specified member'''
        if member == None or discord.utils.get(ctx.message.author.roles, id='334250664870019073') == None:
            member = ctx.message.author
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='298816905504882698'))
        await self.bot.say("I have given {} the **SA2** and **Member** Roles!".format(member.name))
        await self.bot.send_message(discord.utils.get(ctx.message.server.channels, id='298812318903566337'), "Welcome {} to Stu's Army 2!".format(ctx.message.author.mention))
            
    @commands.command(pass_context=True, aliases=['SA3'])
    @commands.check(welcomechannel)
    async def sa3(self, ctx, member:discord.Member = None):
        '''Gives the SA3 role and Member role to the specified member'''
        if member == None or discord.utils.get(ctx.message.author.roles, id='334250664870019073') == None:
            member = ctx.message.author
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='299912276008501248'))
        await self.bot.say("I have given {} the **SA3** and **Member** Roles!".format(member.name))
        await self.bot.send_message(discord.utils.get(ctx.message.server.channels, id='298812318903566337'), "Welcome {} to Stu's Army 3!".format(ctx.message.author.mention))
   
    @commands.command(pass_context=True, aliases=['SA4'])
    @commands.check(welcomechannel)
    async def sa4(self, ctx, member:discord.Member = None):
        '''Gives the SA4 role and Member role to the specified member'''
        if member == None or discord.utils.get(ctx.message.author.roles, id='334250664870019073') == None:
            member = ctx.message.author
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, id='298817009372889088'), discord.utils.get(ctx.message.server.roles, id='329922314747641859'))
        await self.bot.say("I have given {} the **SA4** and **Member** Roles!".format(member.name))
        await self.bot.send_message(discord.utils.get(ctx.message.server.channels, id='298812318903566337'), "Welcome {} to Stu's Army 4!".format(ctx.message.author.mention))
        
def setup(bot):
    bot.add_cog(Commands(bot))
