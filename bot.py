import datetime
import glob
import inspect
import io
import json
import os
import textwrap
import traceback
from contextlib import redirect_stdout

import aiohttp
import clashroyale
import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

from cogs.claninfo import claninfo
from cogs.new_welcome import InvalidTag
from ext.formatter import EmbedHelp

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None, formatter=EmbedHelp())
        self.remove_command('help')
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.mongo = AsyncIOMotorClient('mongodb+srv://fourjr:4SoWl2MNbWybV3xM@dbots-2-giqxl.mongodb.net/')
        self.statsy_mongo = AsyncIOMotorClient('mongodb+srv://read:IFSDUgYdY64tn6Wu@statsy-lpu1v.mongodb.net/')
        self.client = clashroyale.Client('9ba015601c85435aa0ac200afc07223e2b1a3190927c4bb19d89fe5f8295d60e', is_async=True, session=self.session, timeout=5)

        for i in os.listdir('cogs'):
            if i.endswith('.py'):
                cog_name = 'cogs.' + i.replace('.py', '')
                try:
                    self.load_extension(cog_name)
                except Exception as e:
                    print(e)
                else:
                    print(f'Loaded: {cog_name}')


    def token(self):
        '''Returns your token wherever it is'''
        try:
            with open('./data/config.json') as f:
                config = json.load(f)
                return config.get('TOKEN').strip('\"')
        except:
            return os.environ.get('TOKEN')

    async def get_prefix(self, message):
        '''Returns your prefix wherever it is'''
        try:
            with open('data/config.json') as f:
                config = json.load(f)
                return 'b>'
        except:
            return '>'

    def heroku(self):
        '''Using Heroku?'''
        try:
            with open('./data/config.json') as f:
                config = json.load(f)
                return False
        except:
            return True

    def emoji(self, name: str, emojiresp=False):
        if name == 'chestmagic':
            name = 'chestmagical'
        name = name.replace('.', '')
        emoji = discord.utils.get(bot.emojis, name=name)
        if not emojiresp:
            try:
                return str(f'<:{emoji.name}:{emoji.id}>')
            except:
                return name
        else:
            if emoji is not None:
                return emoji
            else:
                return name


    async def invoke(self, ctx):
        '''Overwrites the default invoke for typing'''
        if ctx.command is not None:
            bot.dispatch('command', ctx)
            try:
                if (await bot.can_run(ctx, call_once=True)):
                    async with ctx.typing():
                        await ctx.command.invoke(ctx)
            except commands.CommandError as e:
                await ctx.command.dispatch_error(ctx, e)
            else:
                bot.dispatch('command_completion', ctx)
        elif ctx.invoked_with:
            exc = commands.errors.CommandNotFound('Command "{}" is not found'.format(ctx.invoked_with))
            bot.dispatch('command_error', ctx, exc)

bot = Bot()

@bot.event
async def on_ready():
    bot.uptime = datetime.datetime.now()
    print('''
------------------------------------------
Bot Ready!
------------------------------------------
Username: {}
User ID: {}
------------------------------------------'''.format(bot.user, bot.user.id))


@bot.command()
async def ping(ctx):
    'Pong!'
    msgtime = ctx.message.created_at
    await (await bot.ws.ping())
    now = datetime.datetime.now()
    ping = now - msgtime
    msgtime = datetime.datetime.now()
    now = datetime.datetime.now()
    dblatency = now - msgtime
    pong = discord.Embed(title='Pong!', color=65535)
    pong.add_field(name='Message Latency', value=str("%.2f" % (ping.microseconds / 1000)) + 'ms')
    pong.add_field(name='Discord API Latency', value=str("%.2f" % (bot.latency * 1000)) + 'ms')
    await ctx.send(embed=pong)


@bot.command()
async def help(ctx):
    'Shows.. help?'
    await ctx.send("""
This isn't kept up to date 100% because I'm lazy :)
**Welcome Channel**
`>sa1` to `>sa4` - Give someone member role and clan role.
`>visitor` - Give someone the visitor role

**Non-Welcome Channel**
`>help` - Shows this list of useful information.
`>ping` - Pong!
`>update` - Updates <#365870449915330560>

**All Channels**
`>addrole` - Adds custom roles
`>claninfo` - Sends you the data in <#365870449915330560>
`>invite` - Get the invite code for the server

**Mod Commands**
`>kick` - Kick?
`>ban` - Use this on JJ ;)""")


@bot.command()
async def restart(ctx):
    'Restarts the bot.'
    if (ctx.author.id == 180314310298304512):
        channel = ctx.channel
        await ctx.send('Restarting...')
        await bot.logout()


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await ctx.channel.send(embed=page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await ctx.channel.send(embed=page)


@bot.event
async def on_command_error(ctx, error):
    print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
    erroremb = discord.Embed(description='```py\n' + ''.join(traceback.format_exception(type(error), error, error.__traceback__)) + '\n```', color=discord.Color.red(), timestamp=ctx.message.created_at)
    erroremb.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    erroremb.add_field(name='Message Content', value=ctx.message.content)
    # erroremb.add_field(name='Error', value=)
    erroremb.add_field(name='Location', value=f'#{ctx.channel.name} ({ctx.channel.id})')
    await discord.utils.get(discord.utils.get(bot.guilds, id=359577438101176320).channels, id=375113574038896640).send(embed=erroremb)
    channel = ctx.channel
    if isinstance(error, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.DisabledCommand):
        await channel.send('That command is disabled.')
    elif isinstance(error, InvalidTag):
        await ctx.send(error.message)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.3f}s')
    elif isinstance(error, clashroyale.RequestError):
        await ctx.send('RoyaleAPI is down at the moment. Please try again later.')
    elif isinstance(error, commands.CommandInvokeError):
        no_dms = 'Cannot send messages to this user'
        is_help_cmd = (ctx.command.qualified_name == 'help')
        is_forbidden = isinstance(error.original, discord.Forbidden)
        if (is_help_cmd and is_forbidden and (error.original.text == no_dms)):
            msg = "I couldn't send the help message to you in DM. Either you blocked me or you disabled DMs in this server."
            await channel.send(msg)
            return
    elif isinstance(error, clashroyale.errors.RequestError):
        await ctx.send('API is down at the moment, please try again later.')


@bot.command()
async def coglist(ctx):
    'See unloaded and loaded cogs!'
    if (ctx.author.id == 180314310298304512):

        def pagify(text, delims=['\n'], *, escape=True, shorten_by=8, page_length=2000):
            'DOES NOT RESPECT MARKDOWN BOXES OR INLINE CODE'
            in_text = text
            if escape:
                num_mentions = (text.count('@here') + text.count('@everyone'))
                shorten_by += num_mentions
            page_length -= shorten_by
            while (len(in_text) > page_length):
                closest_delim = max([in_text.rfind(d, 0, page_length) for d in delims])
                closest_delim = (closest_delim if (closest_delim != (- 1)) else page_length)
                if escape:
                    to_send = escape_mass_mentions(in_text[:closest_delim])
                else:
                    to_send = in_text[:closest_delim]
                yield to_send
                in_text = in_text[closest_delim:]
            yield in_text

    def box(text, lang=''):
        ret = '```{}\n{}\n```'.format(lang, text)
        return ret
    loaded = [c.__module__.split('.')[1] for c in bot.cogs.values()]

    def _list_cogs():
        cogs = [os.path.basename(f) for f in glob.glob('cogs/*.py')]
        return [('cogs.' + os.path.splitext(f)[0]) for f in cogs]
    unloaded = [c.split('.')[1] for c in _list_cogs() if (c.split('.')[1] not in loaded)]
    if (not unloaded):
        unloaded = ['None']
    em1 = discord.Embed(color=discord.Color.green(), title='+ Loaded', description=', '.join(sorted(loaded)))
    em2 = discord.Embed(color=discord.Color.red(), title='- Unloaded', description=', '.join(sorted(unloaded)))
    await ctx.send(embed=em1)
    await ctx.send(embed=em2)


@commands.is_owner()
@bot.command(name='eval')
async def _eval(ctx, *, body: str):
    """Evaluates python code"""

    env = {
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        'source': inspect.getsource
    }

    env.update(globals())

    body = cleanup_code(body)
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


def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')


def get_syntax_error(e):
    if e.text is None:
        return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


@commands.is_owner()
@bot.command()
async def say(ctx, *, message: str):
    'Say something as the bot.'
    if (discord.utils.get(ctx.author.roles, id=298817057426767873) != None):
        if ('{}say'.format(ctx.prefix) in message):
            await ctx.send("Don't ya dare spam.")
        else:
            await ctx.send(message)


@bot.command()
async def source(ctx, *, command: str=None):
    'Displays my full source code or for a specific command.\n    To display the source code of a subcommand you can separate it by\n    periods, e.g. tag.create for the create subcommand of the tag command\n    or by spaces.\n    '
    source_url = 'https://github.com/fourjr/stusarmybot'
    if (command is None):
        await ctx.send(source_url)
        return
    obj = bot.get_command(command.replace('.', ' '))
    if (obj is None):
        return await ctx.send('Could not find command.')
    src = obj.callback.__code__
    (lines, firstlineno) = inspect.getsourcelines(src)
    if (not obj.callback.__module__.startswith('discord')):
        location = os.path.relpath(src.co_filename).replace('\\', '/')
    else:
        location = (obj.callback.__module__.replace('.', '/') + '.py')
        source_url = 'https://github.com/fourjr/stusarmybot'
    final_url = '<{}/blob/master/{}#L{}-L{}>'.format(source_url, location, firstlineno, ((firstlineno + len(lines)) - 1))
    await ctx.send(final_url)


@bot.command(name='reload')
async def _reload(ctx, *, module: str):
    'Reloads a module.'
    if (ctx.author.id == 180314310298304512):
        channel = ctx.channel
        module = ('cogs.' + module)
        try:
            bot.unload_extension(module)
            x = await channel.send('Successfully Unloaded.')
            bot.load_extension(module)
            x = await x.edit(content='Successfully Reloaded.')
        except Exception as e:
            x = await x.edit(content='🔫')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            x = await x.edit(content='Done. 👌')


@bot.command()
async def load(ctx, *, module):
    if (ctx.author.id == 180314310298304512):
        'Loads a module.'
        module = ('cogs.' + module)
        try:
            bot.load_extension(module)
            await ctx.send('Successfully Loaded.')
        except Exception as e:
            await ctx.send('🔫\n{}: {}'.format(type(e).__name__, e))


@bot.command()
async def unload(ctx, *, module):
    'Unloads a module.'
    if (ctx.author.id == 180314310298304512):
        module = ('cogs.' + module)
        try:
            bot.unload_extension(module)
            await ctx.send('Successfully Unloaded `{}`'.format(module))
        except:
            pass

if not bot.heroku():
    try:
        bot.unload_extension('cogs.logging')
        bot.unload_extension('cogs.levelling')
    except:
        pass
    else:
        print('Unloaded: {}'.format('cogs.logging'))
        print('Unloaded: {}'.format('cogs.levelling'))
try:
    bot.run(bot.token(), reconnect=True, activity=discord.Game("for Stu's Army!"))
except Exception as e:
    print(e)
