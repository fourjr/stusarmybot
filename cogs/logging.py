import discord
import asyncio
from discord.ext import commands
from utils import checks

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
		await self.bot.add_roles(member, discord.utils.get(member.server.roles, id='345834741829730305'))
		await asyncio.sleep(120)
		tup1 = (0xff0f7f, 0xff0f1a, 0x2ef65c, 0xf5f404, 0x0da1e8, 0xffa200, 0xd96af2)
		await self.bot.add_roles(member, discord.utils.get(member.server.roles, id='317621138274648066'))
		await asyncio.sleep(0.5)
		await self.bot.remove_roles(member, discord.utils.get(member.server.roles, id='345834741829730305'))
		embed=discord.Embed(title="Hello {}!".format(member.name), description="Welcome To {}! Below listed are our Clans!".format(member.server.name , color = random.choice(tup1[0:6]))
		embed.add_field(name="Stu's Army 1", value="3800 Trophies", inline=True)
		embed.add_field(name="Stu's Army 2", value="2800 Trophies", inline=True)
        embed.add_field(name="Stu's Army 3", value="2400 Trophies", inline=True)
        embed.add_field(name="Stu's Army 4", value="2000 Trophies", inline=True)
		welcome = await self.bot.send_message(member.server.get_channel('298816198349553665'), member.mention, embed=embed)
		await self.bot.edit_message(welcome, '\u200B', embed=embed)
			
			

def setup(bot):
bot.add_cog(Logging(bot))
