import discord
from ext.formatter import EmbedHelp
from discord.ext import commands
from contextlib import redirect_stdout
import datetime
import inspect
import os
import glob
import random
import io
import textwrap
import traceback
import asyncio
import random

TOKEN = os.environ['TOKEN']
PREFIX = '>'

bot = commands.Bot(command_prefix=PREFIX, formatter=EmbedHelp())
bot.remove_command('help')

_extensions = [

    'cogs.logging',
    'cogs.commands'

    ]

@bot.event
async def on_ready():
    bot.uptime = datetime.datetime.now()
    print('------------------------------------------\n'
    	  'Bot Ready!\n'
    	  '------------------------------------------\n'
    	  'Username: {}\n'
          'User ID: {}\n'
          '------------------------------------------'
    	  .format(bot.user, bot.user.id))
    await bot.change_presence(game=discord.Game(name="for Stu's Army!"))
    
        
@bot.command(pass_context=True)
async def ping(ctx):
    """Pong!"""
    msgtime = ctx.message.timestamp.now()
    await (await bot.ws.ping())
    now = datetime.datetime.now()
    ping = now - msgtime
    pong = discord.Embed(title='Pong!',
    					 description=str(ping.microseconds / 1000.0) + ' ms',
                         color=0x00ffff)
    await bot.say(embed=pong)

@bot.command(pass_context=True)
async def restart(ctx):
    """Restarts the selfbot."""
    if ctx.message.author.id == '180314310298304512':
        channel = ctx.message.channel
        await bot.say("Restarting...")
        await bot.logout()

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            print(page)
            await bot.send_message(ctx.message.channel, embed=page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            print(page)
            await bot.send_message(ctx.message.channel, embed=page)

@bot.event
async def on_command_error(error, ctx):
    print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
    channel = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.message.content.startswith('trophy'):
            embed=discord.Embed(title=">trophy <current amount of trophies>", description="We will suggest Clans that meet your trophy level!", color=0xe67e22)
            await self.bot.say(embed=embed)
        else: await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(channel, "That command is disabled.")
    elif isinstance(error, commands.CommandInvokeError):
        # A bit hacky, couldn't find a better way
        no_dms = "Cannot send messages to this user"
        is_help_cmd = ctx.command.qualified_name == "help"
        is_forbidden = isinstance(error.original, discord.Forbidden)
        if is_help_cmd and is_forbidden and error.original.text == no_dms:
            msg = ("I couldn't send the help message to you in DM. Either"
                  " you blocked me or you disabled DMs in this server.")
            await bot.send_message(channel, msg)
            return

@bot.command(pass_context=True)
async def coglist(ctx):
    '''See unloaded and loaded cogs!'''
    if ctx.message.author.id == '180314310298304512':
        def pagify(text, delims=["\n"], *, escape=True, shorten_by=8,
                page_length=2000):
            """DOES NOT RESPECT MARKDOWN BOXES OR INLINE CODE"""
            in_text = text
            if escape:
                num_mentions = text.count("@here") + text.count("@everyone")
                shorten_by += num_mentions
            page_length -= shorten_by
            while len(in_text) > page_length:
                closest_delim = max([in_text.rfind(d, 0, page_length)
                                    for d in delims])
                closest_delim = closest_delim if closest_delim != -1 else page_length
                if escape:
                    to_send = escape_mass_mentions(in_text[:closest_delim])
                else:
                    to_send = in_text[:closest_delim]
                yield to_send
                in_text = in_text[closest_delim:]
            yield in_text

    def box(text, lang=""):
        ret = "```{}\n{}\n```".format(lang, text)
        return ret
    loaded = [c.__module__.split(".")[1] for c in bot.cogs.values()]
    # What's in the folder but not loaded is unloaded
    def _list_cogs():
          cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
          return ["cogs." + os.path.splitext(f)[0] for f in cogs]
    unloaded = [c.split(".")[1] for c in _list_cogs()
                if c.split(".")[1] not in loaded]

    if not unloaded:
        unloaded = ["None"]

    em1 = discord.Embed(color=discord.Color.green(), title="+ Loaded", description=", ".join(sorted(loaded)))
    em2 = discord.Embed(color=discord.Color.red(), title="- Unloaded", description=", ".join(sorted(unloaded)))
    await bot.say(embed=em1)
    await bot.say(embed=em2)

def cleanup_code( content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')

def get_syntax_error(e):
    if e.text is None:
        return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
    return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

async def to_code_block(ctx, body):
    if body.startswith('```') and body.endswith('```'):
        content = '\n'.join(body.split('\n')[1:-1])
    else:
        content = body.strip('`')
    await bot.say('```py\n'+content+'```')

@bot.command(pass_context=True, name='eval')
async def _eval(ctx, *, body: str):
    '''Run python scripts on discord!'''
    await to_code_block(ctx, body)
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'server': ctx.message.server,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(content=body)
    stdout = io.StringIO()

    to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

    try:
        exec(to_compile, env)
    except SyntaxError as e:
        return await bot.say(get_syntax_error(e))

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        x = await bot.say(f'```py\n{e}\n{traceback.format_exc()}\n{value}```')
        try:
            await bot.add_reaction(x, '\U0001f534')
        except:
            pass
    else:
        value = stdout.getvalue()

        if TOKEN in value:
            value = value.replace(TOKEN,"[EXPUNGED]")

        if ret is None:
            if value:
                try:
                    x = await bot.say('```py\n%s\n```' % value)
                except:
                    x = await bot.say('```py\n\'Result was too long.\'```')
                try:
                    await bot.add_reaction(x, '\U0001f535')
                except:
                    pass
            else:
                try:
                    await bot.add_reaction(ctx.message, '\U0001f535')
                except:
                    pass
        else:
            try:
                x = await bot.say('```py\n%s%s\n```' % (value, ret))
            except:
                x = await bot.say('```py\n\'Result was too long.\'```')
            try:
                await bot.add_reaction(x, '\U0001f535')
            except:
                pass

@bot.command(pass_context=True)
async def say(ctx, *, message: str):
    '''Say something as the bot.'''
    if discord.utils.get(ctx.message.author.roles, id='298817057426767873') != None:
        if '{}say'.format(ctx.prefix) in message:
            await bot.say("Don't ya dare spam.")
        else:
            await bot.say(message)

@bot.command(pass_context=True)
async def source(ctx, *, command: str = None):
    """Displays my full source code or for a specific command.
    To display the source code of a subcommand you can separate it by
    periods, e.g. tag.create for the create subcommand of the tag command
    or by spaces.
    """
    source_url = 'https://github.com/fourjr/mcplayzbot'
    if command is None:
        await bot.say(source_url)
        return

    obj = bot.get_command(command.replace('.', ' '))
    if obj is None:
        return await bot.say('Could not find command.')

    # since we found the command we're looking for, presumably anyway, let's
    # try to access the code itself
    src = obj.callback.__code__
    lines, firstlineno = inspect.getsourcelines(src)
    if not obj.callback.__module__.startswith('discord'):
        # not a built-in command
        location = os.path.relpath(src.co_filename).replace('\\', '/')
    else:
        location = obj.callback.__module__.replace('.', '/') + '.py'
        source_url = 'https://github.com/fourjr/mcplayzbot'

    final_url = '<{}/blob/master/{}#L{}-L{}>'.format(source_url, location, firstlineno, firstlineno + len(lines) - 1)
    await bot.say(final_url)

@bot.command(pass_context=True,name='reload')
async def _reload(ctx,*, module : str):
    """Reloads a module."""
    if ctx.message.author.id == '180314310298304512':
        channel = ctx.message.channel
        module = 'cogs.'+module
        try:
            bot.unload_extension(module)
            x = await bot.send_message(channel,'Successfully Unloaded.')
            bot.load_extension(module)
            x = await bot.edit_message(x,'Successfully Reloaded.')
        except Exception as e:
            x = await bot.edit_message(x,'\N{PISTOL}')
            await bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            x = await bot.edit_message(x,'Done. \N{OK HAND SIGN}')

@bot.command(pass_context=True)
async def load(ctx, *, module):
    if ctx.message.author.id == '180314310298304512':
        '''Loads a module.'''
        module = 'cogs.'+module
        try:
            bot.load_extension(module)
            await bot.say('Successfully Loaded.')
        except Exception as e:
            await bot.say('\N{PISTOL}\n{}: {}'.format(type(e).__name__, e))

@bot.command(pass_context=True)
async def unload(ctx, *, module):
    '''Unloads a module.'''
    if ctx.message.author.id == '180314310298304512':
        module = 'cogs.'+module
        try:
            bot.unload_extension(module)
            await bot.say('Successfully Unloaded `{}`'.format(module))
        except:
            pass

for extension in _extensions:
    try:
        bot.load_extension(extension)
        print('Loaded: {}'.format(extension))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Error on load: {}\n{}'.format(extension, exc))

try:
    bot.run(TOKEN.strip('\"'))
except Exception as e:
    print('\n[ERROR]: \n{}\n'.format(e))
