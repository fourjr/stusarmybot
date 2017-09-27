from discord.ext import commands
import discord.utils

def is_owner_check(message):
    return message.author.id == '180314310298304512'
  

def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None

def welcomeassistant():
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Welcome Assistant'))

return commands.check(predicate)
