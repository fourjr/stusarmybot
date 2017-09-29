import discord
import random
import asyncio
from discord.ext import commands

class Logging:
	def __init__(self, bot):
		self.bot = bot
		self.sessions = set()
		
	async def on_message_edit(self, before, after):
		if before.channel.id == '362172188301852672': return
		if before.author == self.bot.user: return
		if before.content == after.content: return
		
		embed=discord.Embed(title="Message Edited", color=0xa4029b)
		embed.add_field(name="User", value='{}#{} ({})'.format(before.author.name, before.author.discriminator,  before.author.id), inline=True)
		embed.add_field(name="Message ID", value=after.id, inline=True)
		embed.add_field(name="Channel", value='{} ({})'.format(before.channel,before.channel.id), inline=False)
		embed.add_field(name="Old Message", value=before.content, inline=False)
		embed.add_field(name="New Message", value=after.content, inline=False)
		await self.bot.send_message(before.server.get_channel('362175558043566080'), embed=embed)
	
	async def on_message_delete(self, message):
		if message.channel.id == '362172188301852672': return
		if message.author == message.server.me: return
		
		embed=discord.Embed(title="Message Deleted", color=0xff1a1f)
		embed.add_field(name="User", value='{}#{} ({})'.format(message.author.name, message.author.discriminator,  message.author.id), inline=True)
		embed.add_field(name="Message ID", value=message.id, inline=True)
		embed.add_field(name="Channel", value='{} ({})'.format(message.channel,message.channel.id), inline=False)
		embed.add_field(name="Content", value=message.content, inline=False)
		await self.bot.send_message(message.server.get_channel('362175558043566080'), embed=embed)
		
	async def on_member_join(self, member):
		colors = (0xff0f7f, 0xff0f1a, 0x2ef65c, 0xf5f404, 0x0da1e8, 0xffa200, 0xd96af2)
		embed=discord.Embed(title="Hello {}!".format(member.name), description="Welcome To {} Below listed are our Clans! \n \nDo `>trophy <current amount of trophies>` to get a recommendation to a Clan!".format(member.server.name), color = random.choice(colors[0:6]))
		embed.add_field(name="Stu's Army 1", value="4000 Trophies [Read more](https://statsroyale.com/clan/88PYQV)", inline=True)
		embed.add_field(name="Stu's Army 2", value="2800 Trophies [Read More](https://statsroyale.com/clan/29UQQ282)", inline=True)
		embed.add_field(name="Stu's Army 3", value="2400 Trophies [Read More](https://statsroyale.com/clan/28JU8P0Y)", inline=True)
		embed.add_field(name="Stu's Army 4", value="2000 Trophies [Read More](https://statsroyale.com/clan/8PUUGRYG)", inline=True)
		welcome = await self.bot.send_message(member.server.get_channel('298816198349553665'), '{} <@&334250664870019073> <@277389105501831170>'.format(member.mention), embed=embed)
		await self.bot.edit_message(welcome, '\u200B', embed=embed)
	
	async def on_member_remove(self, member):
		await self.bot.send_message(member.server.get_channel('298816198349553665'), '{} has left us :('.format(member.name))
		
def setup(bot):
	bot.add_cog(Logging(bot))
