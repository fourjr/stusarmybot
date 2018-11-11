import datetime
import inspect
import io
import os
import textwrap
import traceback
from contextlib import redirect_stdout

import aiohttp
import clashroyale
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from cogs.welcome import InvalidTag


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.getenv('PREFIX', '>'))
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.mongo = AsyncIOMotorClient(os.getenv('MONGO'))
        self.statsy_mongo = AsyncIOMotorClient(os.getenv('STATSYMONGO'))
        self.client = clashroyale.OfficialAPI(
            os.getenv('CLASHROYALE'), is_async=True, session=self.session, timeout=10, url=os.getenv('SERVER')
        )

        self.remove_command('help')
        self.add_command(self.ping)
        self.add_command(self._eval)

        protected = ('cogs.logging', 'cogs.levelling')

        for i in os.listdir('cogs'):
            if i.endswith('.py'):
                cog_name = 'cogs.' + i.replace('.py', '')
                if os.name == 'nt' and cog_name in protected:
                    continue
                try:
                    self.load_extension(cog_name)
                except Exception as e:
                    traceback.print_exc()
                else:
                    print(f'Loaded: {cog_name}')

        self.run(os.getenv('TOKEN'), activity=discord.Game("for Stu's Army!"))

    def emoji(self, name: str, emojiresp=False):
        if name == 'chestmagic':
            name = 'chestmagical'
        name = name.replace('.', '')
        emoji = discord.utils.get(self.emojis, name=name)
        if not emojiresp:
            return str(emoji or name)
        return emoji or name

    async def invoke(self, ctx):
        """Overwrites the default invoke for typing"""
        if ctx.command is not None:
            self.dispatch('command', ctx)
            try:
                if (await self.can_run(ctx, call_once=True)):
                    async with ctx.typing():
                        await ctx.command.invoke(ctx)
            except commands.CommandError as e:
                await ctx.command.dispatch_error(ctx, e)
            else:
                self.dispatch('command_completion', ctx)
        elif ctx.invoked_with:
            exc = commands.errors.CommandNotFound('Command "{}" is not found'.format(ctx.invoked_with))
            self.dispatch('command_error', ctx, exc)

    async def on_ready(self):
        self.uptime = datetime.datetime.now()
        print('Ready')

    async def on_command_error(self, ctx, error):
        trace = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        print(trace)
        erroremb = discord.Embed(description=f'```py\n{trace}\n```', color=discord.Color.red(), timestamp=ctx.message.created_at)
        erroremb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        erroremb.add_field(name='Message Content', value=ctx.message.content)
        erroremb.add_field(name='Location', value=f'#{ctx.channel.name} ({ctx.channel.id})')

        await self.get_channel(375113574038896640).send(embed=erroremb)

        if isinstance(error, InvalidTag):
            await ctx.send(error.message)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.3f}s')
        elif isinstance(error, clashroyale.RequestError):
            await ctx.send('RoyaleAPI is down at the moment. Please try again later.')

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        msgtime = ctx.message.created_at
        now = datetime.datetime.now()
        ping = now - msgtime
        pong = discord.Embed(title='Pong!', color=65535)
        pong.add_field(name='Message Latency', value=str("%.2f" % (ping.microseconds / 1000)) + 'ms')
        pong.add_field(name='Discord API Latency', value=str("%.2f" % (self.bot.latency * 1000)) + 'ms')
        await ctx.send(embed=pong)

    @commands.is_owner()
    @commands.command(name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates python code"""

        env = {
            'ctx': ctx,
            'bot': self,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await err.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = ctx.paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = ctx.paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await out.add_reaction('\u2705')
        if err:
            await err.add_reaction('\u2049')

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    try:
        Bot()
    except Exception as e:
        traceback.print_exc()
