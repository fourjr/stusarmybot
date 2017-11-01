import discord
from discord.ext import commands
import crasync
import asyncio

class Stats():
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    async def checktag(self, tag, channel):
        if any(letter not in 'PYLQGRJCUV0289' for letter in tag):
            await channel.send('Invalid Player Tag!')
            return False
        else:
            return True
    
    async def checkclantag(self, tag, channel):
        if any(letter not in 'PYLQGRJCUV0289' for letter in tag):
            await channel.send('Invalid Clan Tag!')
            return False
        else:
            return True

    
    def clanprofileurl(self, profile):
        if profile.clan_badge_url == None:
            return 'https://raw.githubusercontent.com/kwugfighter/cr-selfstats/master/data/clanless.png'
        else:
            return profile.clan_badge_url
        
    @commands.command()
    async def save(self, ctx, tag:str):
        '''Saves your tag!'''
        tag = tag.replace('#', '').replace('O', '0').upper()
        if await self.checktag(tag, ctx.channel):
            await self.bot.getdata(f"make stusarmybottags | {ctx.author.id} | {tag}")
            await ctx.send(f'Linked tag `#{tag}` to {ctx.author.name}!')

    @commands.has_any_role("SA1 | Leader", "SA2 | Leader", "SA3 | Leader", "SA4 | Leader", "SA5 | Leader") 
    @commands.command()
    async def savefor(self, ctx, member:discord.Member, tag:str):
        '''Saves the tag for someone!'''
        tag = tag.replace('#', '').replace('O', '0').upper()
        if await self.checktag(tag, ctx.channel):
            await self.bot.getdata(f"make stusarmybottags | {member.id} | {tag}")
            await ctx.send(f'{ctx.author.name} linked tag `#{tag}` to {member.name}!')

    @commands.command()
    async def profile(self, ctx, tag = None):
        '''Shows your Clash Royale Profile'''
        async with ctx.channel.typing():
            emoji = self.bot.emoji
            if len(ctx.message.raw_mentions) == 1 or tag is None:
                if len(ctx.message.raw_mentions) == 1:
                    member = discord.utils.get(ctx.guild.members, id=ctx.message.raw_mentions[0])
                    errormsg = f'{member.name} has not registered a tag!'
                else:
                    member = ctx.author
                    errormsg = 'You have not registered a tag! Do `>save #tag` or `>profile #tag`!'

                await self.bot.getdata(f'read stusarmybottags | {member.id} |')
                try:
                    tagmsg = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
                except asyncio.TimeoutError:
                    return await ctx.send(errormsg)
                tag = tagmsg.content

            tag = tag.replace('#', '').replace('O', '0').upper()
            if not await self.checktag(tag, ctx.channel): return

            try:
                crprof = await self.bot.client.get_profile(tag)
            except Exception as error:
                return await ctx.send(error)
            try:
                constants = await self.bot.client.get_constants()
            except Exception as error:
                return await ctx.send(error)

            deck = ''
            for i in range(8):
                deck += f"{emoji(crprof.deck[i].name.lower().replace(' ', ''))}{crprof.deck[i].level}"

            index = crprof.chest_cycle.position % len(constants.chest_cycle)

            claninfo = f"Clan: {crprof.clan_name} (#{crprof.clan_tag}) \nRole: {crprof.clan_role}"

            profile = discord.Embed(description=f'[StatsRoyale Profile](https://statsroyale.com/profile/{tag})', color=0xe74c3c)
            profile.set_author(name=f"{crprof.name} (#{crprof.tag})", icon_url = ctx.author.avatar_url)
            profile.set_thumbnail(url=self.clanprofileurl(crprof))
            profile.add_field(name='Trophies', value=f"{crprof.current_trophies}/{crprof.highest_trophies} PB {emoji('trophy')}", inline=True)
            profile.add_field(name='Clan Info', value=claninfo)
            profile.add_field(name=f"Chests ({crprof.chest_cycle.position} opened)", value=f"{' '.join([emoji('chest' + crprof.get_chest(x).lower()) for x in range(10)])} \n{emoji('chestsupermagical')} +{crprof.chest_cycle.super_magical-crprof.chest_cycle.position} {emoji('chestlegendary')} +{crprof.chest_cycle.legendary-crprof.chest_cycle.position} {emoji('chestepic')} +{crprof.chest_cycle.epic-crprof.chest_cycle.position} {emoji('chestmagical')} +{crprof.chest_cycle.magical-crprof.chest_cycle.position}")
            profile.add_field(name='Deck', value=deck)
            profile.add_field(name='Shop Offers (Days)', value=f"{emoji('chestlegendary')}{crprof.shop_offers.legendary} {emoji('chestepic')}{crprof.shop_offers.epic} {emoji('arena11')}{crprof.shop_offers.arena}", inline=False)
            profile.add_field(name='Wins/Losses/Draws', value=f"{crprof.wins}/{crprof.losses}/{crprof.draws} ({crprof.win_streak} win streak)")
            await ctx.send(embed=profile)

    @commands.command()
    async def clan(self, ctx, clantag=None):
        '''Shows some Clan Statistics'''
        async with ctx.channel.typing():
            emoji = self.bot.emoji
            foundclan = False
            if clantag is not None:
                if clantag.lower() == 'sa1' or clantag.lower() == 'sa2' or clantag.lower() == 'sa3' or clantag.lower() == 'sa4' or clantag.lower() == 'sa5':
                    if clantag.lower() == 'sa1': clantag = '88PYQV'
                    if clantag.lower() == 'sa2': clantag = '29UQQ282'
                    if clantag.lower() == 'sa3': clantag = '28JU8P0Y'
                    if clantag.lower() == 'sa4': clantag = '8PUUGRYG'
                    if clantag.lower() == 'sa5': clantag = '8YUU2CQV'
                    foundclan = True

            if not foundclan:
                tag = None
                if len(ctx.message.raw_mentions) == 1 or clantag is None:
                    if len(ctx.message.raw_mentions) == 1:
                        member = discord.utils.get(ctx.guild.members, id=ctx.message.raw_mentions[0])
                        errormsg = f'{member.name} has not registered a tag!'
                    else:
                        member = ctx.author
                        errormsg = 'You have not registered a tag! Do `>save #tag` or `>profile #tag`!'

                    await self.bot.getdata(f'read stusarmybottags | {member.id} |')
                    try:
                        tagmsg = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
                    except asyncio.TimeoutError:
                        return await ctx.send(errormsg)
                    tag = tagmsg.content
                    try:
                        clantag = (await self.bot.client.get_profile(tag)).clan_tag
                    except Exception as error:
                        return await ctx.send(error)

                elif clantag is not None:
                    clantag = clantag.replace('#', '').replace('O', '0').upper()
                    if not await self.checkclantag(clantag, ctx.channel):
                        return

            try:
                crclan = await self.bot.client.get_clan(clantag)
            except Exception as error:
                return await ctx.send(error)
            

            clan = discord.Embed(description = crclan.description, color=0x3498db)
            clan.set_author(name=f"{crclan.name} (#{crclan.tag})")
            clan.set_thumbnail(url=crclan.badge_url)
            clan.add_field(name='Type', value=crclan.type_name)
            clan.add_field(name='Score', value=f"{crclan.score} Trophies")
            clan.add_field(name='Donations/Week', value=f"{crclan.donations} Cards")
            clan.add_field(name='Clan Chest', value=f"{crclan.clan_chest.crowns}/{crclan.clan_chest.required}")
            clan.add_field(name='Location', value=crclan.region)
            clan.add_field(name='Members', value=f"{len(crclan.members)}/50")
            await ctx.send(embed=clan)

        
    @commands.command(aliases=['chest'])
    async def chests(self, ctx, number = 10, tag = None):
        '''Shows some of your upcoming/special chests'''
        async with ctx.channel.typing():
            emoji = self.bot.emoji
            if len(ctx.message.raw_mentions) == 1 or tag is None:
                if len(ctx.message.raw_mentions) == 1:
                    member = discord.utils.get(ctx.guild.members, id=ctx.message.raw_mentions[0])
                    errormsg = f'{member.name} has not registered a tag!'
                else:
                    member = ctx.author
                    errormsg = 'You have not registered a tag! Do `>save #tag` or `>profile #tag`!'

                await self.bot.getdata(f'read stusarmybottags | {member.id} |')
                try:
                    tagmsg = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
                except asyncio.TimeoutError:
                    return await ctx.send(errormsg)
                tag = tagmsg.content

            tag = tag.replace('#', '').replace('O', '0').upper()
            if not await self.checktag(tag, ctx.channel): return

            try:
                crprof = await self.bot.client.get_profile(tag)
            except Exception as error:
                return await ctx.send(error)

            try:
                constants = await self.bot.client.get_constants()
            except Exception as error:
                return await ctx.send(error)

            if number > 30: number = 30
            chestemb = discord.Embed(description = f"{crprof.chest_cycle.position} Chests Opened", color=0xf1c40f)
            chestemb.set_author(name=f"{crprof.name} (#{crprof.tag})", icon_url = ctx.author.avatar_url)
            chestemb.set_thumbnail(url=self.clanprofileurl(crprof))
            chestemb.add_field(name=f'Upcoming Chests ({number})', value=' '.join([emoji('chest' + crprof.get_chest(x).lower()) for x in range(number)]))
            chestemb.add_field(name=f"Special Chests", value=f"{emoji('chestsupermagical')} +{crprof.chest_cycle.super_magical-crprof.chest_cycle.position} {emoji('chestlegendary')} +{crprof.chest_cycle.legendary-crprof.chest_cycle.position} {emoji('chestepic')} +{crprof.chest_cycle.epic-crprof.chest_cycle.position} {emoji('chestmagical')} +{crprof.chest_cycle.magical-crprof.chest_cycle.position}")
            await ctx.send(embed=chestemb)

    @commands.command()
    async def usertag(self, ctx, *, member:discord.Member = None):
        if member == None: member = ctx.author
        await self.bot.getdata(f'read stusarmybottags | {member.id} |')
        try:
            tagmsg = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
        except asyncio.TimeoutError:
            await ctx.send(f'{member.name} have not registered a tag! Do `>save #tag` or `>profile #tag`!')
            return
        await ctx.send(f"{member.name}'s tag is `#{tagmsg.content}`")

    @commands.has_any_role("SA1 | Leader", "SA2 | Leader", "SA3 | Leader", "SA4 | Leader", "SA5 | Leader") 
    @commands.command()
    async def checkdb(self, ctx, option=None):
        await self.bot.getdata('.view -db stusarmybottags')
        try:
            database = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
        except asyncio.TimeoutError:
            return await ctx.send('DB Down')
        
        message = ''
        db = database.content.split('\n')
        for i in range(len(db)):
            db[i] = db[i].split(': ')

        if option == None or option == 'list':
            for i in range(len(db)):
                try:
                    message += f'{discord.utils.get(ctx.guild.members, id=int(db[i][0])).name}: {db[i][1]}\n'
                except:
                    pass
            await ctx.send('```\n' +message + '\n```')

        elif option == 'total':
            await ctx.send(f'{len(db)} tags stored')

def setup(bot):
    bot.add_cog(Stats(bot))
