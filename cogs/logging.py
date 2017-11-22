import discord
import random
import asyncio
import craysnc
import aiohttp
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
        embed = discord.Embed(title='Hello {}!'.format(member.name), description='Welcome To {} Below listed are our Clans! \n \nDo `?save <your player tag>` (e.g. `?save 2P0LYQ`) to help us select a clan for you!'.format(member.guild.name), color=random.choice(colors[0:6]))
        try:
            sa1 = (await self.bot.client.get_clan('88PYQV')).required_trophies
            sa2 = (await self.bot.client.get_clan('29UQQ282')).required_trophies
            sa3 = (await self.bot.client.get_clan('28JU8P0Y')).required_trophies
            sa4 = (await self.bot.client.get_clan('8PUUGRYG')).required_trophies
            sa5 = (await self.bot.client.get_clan('8YUU2CQV')).required_trophies
        except Exception as e:
            embed.add_field(name="Stu's Army!", value= '[Read more](https://statsroyale.com/clan/88PYQV)')
            embed.add_field(name="Stu's Army! II", value=f'[Read More](https://statsroyale.com/clan/29UQQ282)')
            embed.add_field(name="Stu's Army! III", value=f'[Read More](https://statsroyale.com/clan/28JU8P0Y)')
            embed.add_field(name="Stu's Army! IV", value=f'[Read More](https://statsroyale.com/clan/8PUUGRYG)')
            embed.add_field(name="Stu's Army! V", value=f'[Read More](https://statsroyale.com/clan/8YUU2CQV)')
            embed.set_footer(text='API currently down: ' + e)
        else:
            embed.add_field(name="Stu's Army!", value=f'{sa1} Trophies [Read more](https://statsroyale.com/clan/88PYQV)')
            embed.add_field(name="Stu's Army! II", value=f'{sa2} Trophies [Read More](https://statsroyale.com/clan/29UQQ282)')
            embed.add_field(name="Stu's Army! III", value=f'{sa3} Trophies [Read More](https://statsroyale.com/clan/28JU8P0Y)')
            embed.add_field(name="Stu's Army! IV", value=f'{sa4} Trophies [Read More](https://statsroyale.com/clan/8PUUGRYG)')
            embed.add_field(name="Stu's Army! V", value=f'{sa5} Trophies [Read More](https://statsroyale.com/clan/8YUU2CQV)')
        
        welcome = await member.guild.get_channel(298816198349553665).send('{} <@&334250664870019073> <@277389105501831170>'.format(member.mention), embed=embed)
        await welcome.edit(embed=embed, content='\u200b')

    async def on_member_remove(self, member):
        await member.guild.get_channel(298816198349553665).send('{} has left us :('.format(member.name))

def setup(bot):
    bot.add_cog(Logging(bot))
