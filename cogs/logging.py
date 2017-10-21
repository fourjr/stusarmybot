import discord
import random
import asyncio
from discord.ext import commands

class Logging():

    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    async def on_message_edit(self, before, after):
        if before.guild.id != 298812318903566337 or before.channel.id == 362172188301852672 or before.author == self.bot.user or before.content == after.content:
            return
        embed = discord.Embed(title='Message Edited', color=10748571)
        embed.add_field(name='User', value='{}#{} ({})'.format(before.author.name, before.author.discriminator, before.author.id), inline=True)
        embed.add_field(name='Message ID', value=after.id, inline=True)
        embed.add_field(name='Channel', value='{} ({})'.format(before.channel, before.channel.id), inline=False)
        embed.add_field(name='Old Message', value=before.content, inline=False)
        embed.add_field(name='New Message', value=after.content, inline=False)
        await before.guild.get_channel(362175558043566080).send(embed=embed)

    async def on_message_delete(self, message):
        if message.guild.id != 298812318903566337 or message.channel.id == 362172188301852672 or message.author == self.bot.user:
            return
        embed = discord.Embed(title='Message Deleted', color=16718367)
        embed.add_field(name='User', value='{}#{} ({})'.format(message.author.name, message.author.discriminator, message.author.id), inline=True)
        embed.add_field(name='Message ID', value=message.id, inline=True)
        embed.add_field(name='Channel', value='{} ({})'.format(message.channel, message.channel.id), inline=False)
        embed.add_field(name='Content', value=message.content, inline=False)
        await message.guild.get_channel(362175558043566080).send(embed=embed)

    async def on_member_join(self, member):
        colors = (16715647, 16715546, 3077724, 16118788, 893416, 16753152, 14248690)
        embed = discord.Embed(title='Hello {}!'.format(member.name), description='Welcome To {} Below listed are our Clans! \n \nDo `>trophy <current amount of trophies>` to get a recommendation to a Clan!'.format(member.guild.name), color=random.choice(colors[0:6]))
        embed.add_field(name="Stu's Army 1", value='4000 Trophies [Read more](https://statsroyale.com/clan/88PYQV)', inline=True)
        embed.add_field(name="Stu's Army 2", value='2800 Trophies [Read More](https://statsroyale.com/clan/29UQQ282)', inline=True)
        embed.add_field(name="Stu's Army 3", value='2400 Trophies [Read More](https://statsroyale.com/clan/28JU8P0Y)', inline=True)
        embed.add_field(name="Stu's Army 4", value='2000 Trophies [Read More](https://statsroyale.com/clan/8PUUGRYG)', inline=True)
        embed.add_field(name="Stu's Army 5", value='Coming real soon! [Soon!](https://statsroyale.com/clan/SOON)', inline=True)
        welcome = await member.guild.get_channel(298816198349553665).send('{} <@&334250664870019073> <@277389105501831170>'.format(member.mention), embed=embed)
        await welcome.edit(embed=embed, content='\u200b')

    async def on_member_remove(self, member):
        await member.guild.get_channel(298816198349553665).send('{} has left us :('.format(member.name))

def setup(bot):
    bot.add_cog(Logging(bot))
