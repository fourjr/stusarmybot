import discord
from discord.ext import commands
import asyncio

class CustomContext(commands.Context):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return self.bot.session

    @staticmethod
    def paginate(text: str):
        '''Simple generator that paginates text.'''

        last = 0

        pages = []

        for curr in range(0, len(text)):

            if curr % 1980 == 0:

                pages.append(text[last:curr])

                last = curr

                appd_index = curr

        if appd_index != len(text)-1:

            pages.append(text[last:curr])

        return list(filter(lambda a: a != '', pages))

