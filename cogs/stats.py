import discord
import asyncio
from discord.ext import commands
import aiohttp
import json

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
        if profile['clan'] == None:
            return 'https://raw.githubusercontent.com/kwugfighter/cr-selfstats/master/data/clanless.png'
        else:
            return f"http://api.cr-api.com{profile['clan']['badge']['url']}"

    def clanclanurl(self, clan):
        return f"http://api.cr-api.com{clan['badge']['url']}"

    @commands.command()
    async def save(self, ctx, tag:str):
        '''Saves your tag!'''
        tag = tag.replace('#', '').replace('O', '0').upper()
        if await self.checktag(tag, ctx.channel):
            await self.bot.web(f"make stusarmybottags | {ctx.author.id} | {tag}")
            await ctx.send(f'Linked {tag} to {ctx.author.name}!')

    @commands.command()
    async def profile(self, ctx, tag = None):
        '''Shows your Clash Royale Profile'''
        async with ctx.channel.typing():
            emoji = self.bot.emoji
            db = False
            if len(ctx.message.raw_mentions) == 1:
                member = discord.utils.get(ctx.guild.members, id=ctx.message.raw_mentions[0])
                errormsg = f'{member.name} has not registered a tag!'
                db = True
                await self.bot.web(f'read stusarmybottags | {member.id} |')

            if tag == None or db:
                if not db:
                    await self.bot.web(f'read stusarmybottags | {ctx.author.id} |')
                try:
                    tagmsg = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
                except asyncio.TimeoutError:
                    await ctx.send('You have not registered a tag! Do `>save #tag` or `>profile #tag`!')
                    return
                tag = tagmsg.content

            tag = tag.replace('#', '').replace('O', '0').upper()
            if not await self.checktag(tag, ctx.channel):
                return

            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.cr-api.com/profile/{tag}") as d:
                    crprof = await d.json()
            
            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.cr-api.com/constants') as d:
                    constants = await d.json()

            chests = ''
            index = crprof['chestCycle']['position'] % len(constants['chestCycle']['order'])
            chestindex = crprof['chestCycle']['position']

            for i in range(10):
                if chestindex == crprof['chestCycle']['superMagicalPos']:
                    chests += emoji('chestsupermagical') + ' '
                elif chestindex == crprof['chestCycle']['legendaryPos']:
                    chests += emoji('chestlegendary') + ' '
                elif chestindex == crprof['chestCycle']['epicPos']:
                    chests += emoji('chestepic') + ' '
                else:
                    chests += emoji('chest' + constants['chestCycle']['order'][index].lower()) + ' '
                index += 1
                chestindex += 1

            deck = ''
            for i in range(8):
                deck += f"{emoji(crprof['currentDeck'][i]['name'].lower().replace(' ', ''))}{crprof['currentDeck'][i]['level']} "

            index = crprof['chestCycle']['position'] % len(constants['chestCycle']['order'])
            smc = crprof['chestCycle']['superMagicalPos'] - crprof['chestCycle']['position']
            legendary = crprof['chestCycle']['legendaryPos'] - crprof['chestCycle']['position']
            epic = crprof['chestCycle']['epicPos'] - crprof['chestCycle']['position']

            winstreak = crprof['games']['currentWinStreak']
            if winstreak < 0: winstreak = 0
            profile = discord.Embed(description=f'[StatsRoyale Profile](https://statsroyale.com/profile/{tag})', color=0xe74c3c)
            profile.set_author(name=f"{crprof['name']} (#{crprof['tag']})", icon_url = ctx.author.avatar_url)
            profile.set_thumbnail(url=self.clanprofileurl(crprof))
            profile.add_field(name='Trophies', value=f"{crprof['trophies']}/{crprof['stats']['maxTrophies']} PB {emoji('trophy')}", inline=True)
            profile.add_field(name='Clan Info', value=f"Clan: {crprof['clan']['name']} (#{crprof['clan']['tag']}) \nRole: {crprof['clan']['role']}")
            profile.add_field(name=f"Chests ({crprof['chestCycle']['position']} opened)", value=f"{chests} \n{emoji('chestsupermagical')} +{smc} {emoji('chestlegendary')} +{legendary} {emoji('chestepic')} +{epic}")
            profile.add_field(name='Deck', value=deck)
            profile.add_field(name='Shop Offers (Days)', value=f"{emoji('chestlegendary')}{crprof['shopOffers']['legendary']} {emoji('chestepic')}{crprof['shopOffers']['epic']} {emoji('arena11')}{crprof['shopOffers']['arena']}")
            profile.add_field(name='Wins/Losses/Draws', value=f"{crprof['games']['wins']}/{crprof['games']['losses']}/{crprof['games']['draws']} ({winstreak} win streak)")
            await ctx.send(embed=profile)

    @commands.command()
    async def clan(self, ctx, clantag=None):
        '''Shows some Clan Statistics'''
        async with ctx.channel.typing():
            emoji = self.bot.emoji
            db = False
            tag = None
            if len(ctx.message.raw_mentions) == 1:
                member = discord.utils.get(ctx.guild.members, id=ctx.message.raw_mentions[0])
                errormsg = f'{member.name} has not registered a tag!'
                db = True
                await self.bot.web(f'read stusarmybottags | {member.id} |')

            if clantag == None or db:
                if not db:
                    await self.bot.web(f'read stusarmybottags | {ctx.author.id} |')
                try:
                    tagmsg = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
                except asyncio.TimeoutError:
                    await ctx.send('You have not registered a tag! Do `>save #tag` or `>profile #tag`!')
                    return
                tag = tagmsg.content
            
            if tag is not None:
                tag = tag.replace('#', '').replace('O', '0').upper()
                if not await self.checktag(tag, ctx.channel):
                    return
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://api.cr-api.com/profile/{tag}") as d:
                        crprof = await d.json()

                clantag = crprof['clan']['tag']

            clantag = clantag.replace('#', '').replace('O', '0').upper()
            if not await self.checkclantag(clantag, ctx.channel):
                return

            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.cr-api.com/clan/{clantag}") as d:
                    crclan = await d.json()
            tiers = [70, 160, 270, 400, 550, 720, 910, 1120, 1350, 1600] 

            clan = discord.Embed(description = crclan['description'], color=0x3498db)
            clan.set_author(name=f"{crclan['name']} (#{crclan['tag']})")
            clan.set_thumbnail(url=self.clanclanurl(crclan))
            clan.add_field(name='Type', value=crclan['typeName'])
            clan.add_field(name='Score', value=f"{crclan['score']} Trophies")
            clan.add_field(name='Donations/Week', value=f"{crclan['donations']} Cards")
            clan.add_field(name='Clan Chest', value=f"Tier {(tiers.index(max([n for n in tiers if (crclan['clanChest']['clanChestCrowns'] > n)])) + 1)}")
            clan.add_field(name='Location', value=crclan['region']['name'])
            clan.add_field(name='Members', value=f"{crclan['memberCount']}/50")
            await ctx.send(embed=clan)

        
    @commands.command(aliases=['chest'])
    async def chests(self, ctx, number = 10, tag = None):
        '''Shows some of your upcoming/special chests'''
        async with ctx.channel.typing():
            emoji = self.bot.emoji
            db = False
            if len(ctx.message.raw_mentions) == 1:
                member = discord.utils.get(ctx.guild.members, id=ctx.message.raw_mentions[0])
                errormsg = f'{member.name} has not registered a tag!'
                db = True
                await self.bot.web(f'read stusarmybottags | {member.id} |')

            if tag == None or db:
                if not db:
                    await self.bot.web(f'read stusarmybottags | {ctx.author.id} |')
                try:
                    tagmsg = await self.bot.wait_for('message', check=self.bot.check, timeout = 2)
                except asyncio.TimeoutError:
                    await ctx.send('You have not registered a tag! Do `>save #tag` or `>profile #tag`!')
                    return
                tag = tagmsg.content

            tag = tag.replace('#', '').replace('O', '0').upper()
            if not await self.checktag(tag, ctx.channel):
                return

            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.cr-api.com/profile/{tag}") as d:
                    crprof = await d.json()

            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.cr-api.com/constants') as d:
                    constants = await d.json()

            chests = ''
            index = crprof['chestCycle']['position'] % len(constants['chestCycle']['order'])
            chestindex = crprof['chestCycle']['position']
            
            if number > 30: number = 30

            for i in range(number):
                if chestindex == crprof['chestCycle']['superMagicalPos']:
                    chests += emoji('chestsupermagical') + ' '
                elif chestindex == crprof['chestCycle']['legendaryPos']:
                    chests += emoji('chestlegendary') + ' '
                elif chestindex == crprof['chestCycle']['epicPos']:
                    chests += emoji('chestepic') + ' '
                else:
                    chests += emoji('chest' + constants['chestCycle']['order'][index].lower()) + ' '
                index += 1
                chestindex += 1
            
            index = crprof['chestCycle']['position'] % len(constants['chestCycle']['order'])
            smc = crprof['chestCycle']['superMagicalPos'] - crprof['chestCycle']['position']
            legendary = crprof['chestCycle']['legendaryPos'] - crprof['chestCycle']['position']
            epic = crprof['chestCycle']['epicPos'] - crprof['chestCycle']['position']

            chestemb = discord.Embed(description = f"{crprof['chestCycle']['position']} Chests Opened", color=0xf1c40f)
            chestemb.set_author(name=f"{crprof['name']} (#{crprof['tag']})", icon_url = ctx.author.avatar_url)
            chestemb.set_thumbnail(url=self.clanprofileurl(crprof))
            chestemb.add_field(name=f'Upcoming Chests ({number})', value=chests)
            chestemb.add_field(name='Special Chests', value=f"{emoji('chestsupermagical')} +{smc} {emoji('chestlegendary')} +{legendary} {emoji('chestepic')} +{epic}")
            await ctx.send(embed=chestemb)

def setup(bot):
    bot.add_cog(Stats(bot))
