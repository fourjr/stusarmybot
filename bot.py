import datetime
import glob
import inspect
import io
import os
import random
import textwrap
import aiohttp
import json
import traceback
from contextlib import redirect_stdout
import discord
from discord.ext import commands
from ext.formatter import EmbedHelp

def token():
    '''Returns your token wherever it is'''
    try:
        with open('./data/config.json') as f:
            config = json.load(f)
            return config.get('TOKEN').strip('\"')
    except:
        return os.environ.get('TOKEN')

def prefix():
    '''Returns your token wherever it is'''
    try:
        with open('data/config.json') as f:
            config = json.load(f)
            return 'b>'
    except:
        return '>' 

def heroku():
    '''Using Heroku?'''
    try:
        with open('./data/config.json') as f:
            config = json.load(f)
            return False
    except:
        return True

bot = commands.Bot(command_prefix=prefix(), formatter=EmbedHelp())
bot.remove_command('help')

async def webhook(content):
    '''Grabs from Database'''
    async with aiohttp.ClientSession() as session:
        url = 'https://canary.discordapp.com/api/webhooks/370568981045575681/21TEod8EkGSLNWQ_CWyepYPkqkukJJLNYs54K7xWG8qadWesoesgZ90bAQ4ctDsh_OUC'
        payload = {
            'content': content,
        }
        headers = {
            'content-type': 'application/json',
        }
        async with session.post(url, data=json.dumps(payload), headers=headers) as r:
            resp = r
            resp.close()

def check(msg):
    return msg.author.id == 249891250117804032 and msg.channel.id == 370240126795776000

bot.web = webhook
bot.check = check

_extensions = ['cogs.logging', 'cogs.commands', 'cogs.claninfo']

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
    await bot.change_presence(game=discord.Game(name="for Stu's Army!"))

@bot.command()
async def ping(ctx):
    'Pong!'
    msgtime = ctx.message.created_at
    await (await bot.ws.ping())
    now = datetime.datetime.now()
    ping = (now - msgtime)
    pong = discord.Embed(title='Pong!', description=(str((ping.microseconds / 1000.0)) + ' ms'), color=65535)
    await ctx.send(embed=pong)

@bot.command()
async def help(ctx):
    'Shows.. help?'
    await ctx.send("""
This isn't kept up to date 100% because I'm lazy :)
**Welcome Channel**
`>sa1` to `>sa5` - Give appropriate roles
`>visitor` - Give appropriate roles

**Non-Welcome Channel**
`>help` - Shows this ~~never updated~~ list of useful information.
`>ping` - Pong!
`>update` - Updates <#365870449915330560>
`>sa1info` to `>sa4info` - Gives you Clan Stats for the various Clans. """)

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
            print(page)
            await ctx.channel.send(embed=page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            print(page)
            await ctx.channel.send(embed=page)

@bot.event
async def on_command_error(ctx, error):
    print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
    channel = ctx.channel
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.message.content.startswith('>trophy'):
            embed = discord.Embed(title='>trophy <current amount of trophies>', description='We will suggest Clans that meet your trophy level!', color=15105570)
            await channel.send(embed=embed)
        else:
            await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.DisabledCommand):
        await channel.send('That command is disabled.')
    elif isinstance(error, commands.CommandInvokeError):
        no_dms = 'Cannot send messages to this user'
        is_help_cmd = (ctx.command.qualified_name == 'help')
        is_forbidden = isinstance(error.original, discord.Forbidden)
        if (is_help_cmd and is_forbidden and (error.original.text == no_dms)):
            msg = "I couldn't send the help message to you in DM. Either you blocked me or you disabled DMs in this server."
            await channel.send(msg)
            return

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

def cleanup_code(content):
    'Automatically removes code blocks from the code.'
    if (content.startswith('```') and content.endswith('```')):
        return '\n'.join(content.split('\n')[1:(- 1)])
    return content.strip('` \n')

def get_syntax_error(e):
    if (e.text is None):
        return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
    return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

async def to_code_block(ctx, body):
    if (body.startswith('```') and body.endswith('```')):
        content = '\n'.join(body.split('\n')[1:(- 1)])
    else:
        content = body.strip('`')
    await ctx.send((('```py\n' + content) + '```'))

@bot.command(name='eval')
async def _eval(ctx, *, body: str):
    'Run python scripts on discord!'
    await to_code_block(ctx, body)
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'server': ctx.guild,
        'message': ctx.message,
    }
    env.update(globals())
    body = cleanup_code(content=body)
    stdout = io.StringIO()
    to_compile = ('async def func():\n%s' % textwrap.indent(body, '  '))
    try:
        exec(to_compile, env)
    except SyntaxError as e:
        return await ctx.send(get_syntax_error(e))
    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        x = await ctx.send(f'''```py
{e}
{traceback.format_exc()}
{value}```''')
        try:
            await x.add_reaction('🔴')
        except:
            pass
    else:
        value = stdout.getvalue()
        if (TOKEN in value):
            value = value.replace(TOKEN, '[EXPUNGED]')
        if (ret is None):
            if value:
                try:
                    x = await ctx.send(('```py\n%s\n```' % value))
                except:
                    x = await ctx.send("```py\n'Result was too long.'```")
                try:
                    await x.add_reaction('🔵')
                except:
                    pass
            else:
                try:
                    await ctx.message.add_reaction('🔵')
                except:
                    pass
        else:
            try:
                x = await ctx.send(('```py\n%s%s\n```' % (value, ret)))
            except:
                x = await ctx.send("```py\n'Result was too long.'```")
            try:
                await x.add_reaction('🔵')
            except:
                pass

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
    source_url = 'https://github.com/fourjr/mcplayzbot'
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
        source_url = 'https://github.com/fourjr/mcplayzbot'
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
for extension in _extensions:
    try:
        bot.load_extension(extension)
        print('Loaded: {}'.format(extension))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Error on load: {}\n{}'.format(extension, exc))

if not heroku():
    try:
        bot.load_extension('cogs.stats')
        print('Loaded: {}'.format('cogs.stats'))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Error on load: {}\n{}'.format('cogs.stats', exc))

try:
    bot.run(token(), reconnect=True)
except Exception as e:
    print(e)
