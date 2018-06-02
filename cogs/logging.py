import random

import discord

class Logging:

    def __init__(self, bot):
        self.bot = bot

    async def on_message_edit(self, before, after):
        if before.channel.id == 362172188301852672 or before.author == self.bot.user or before.content == after.content:
            return
        embed = discord.Embed(title='Message Edited', color=0xa4029b)
        embed.add_field(name='User', value=f'{message.author} ({message.author.id})')
        embed.add_field(name='Message ID', value=after.id)
        embed.add_field(name='Channel', value='{} ({})'.format(before.channel, before.channel.id), inline=False)
        embed.add_field(name='Old Message', value=before.content, inline=False)
        embed.add_field(name='New Message', value=after.content, inline=False)
        await before.guild.get_channel(362175558043566080).send(embed=embed)

    async def on_message_delete(self, message):
        if message.channel.id == 362172188301852672 or message.author == self.bot.user:
            return
        embed = discord.Embed(title='Message Deleted', color=0xff1a1f)
        embed.add_field(name='User', value=f'{message.author} ({message.author.id})'
        embed.add_field(name='Message ID', value=message.id)
        embed.add_field(name='Channel', value='{} ({})'.format(message.channel, message.channel.id), inline=False)
        embed.add_field(name='Content', value=message.content, inline=False)
        await message.guild.get_channel(362175558043566080).send(embed=embed)

def setup(bot):
    bot.add_cog(Logging(bot))
