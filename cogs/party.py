import discord
from discord.ext import commands
from datetime import datetime

from cogs.api import API
from cogs.admin import roles
from cogs.calcs import Calcs

class Party(commands.Cog):

    @commands.command(name='party', aliases=['pl'], hidden=True)
    async def party_list(self, ctx):
            await ctx.send("For some reason, this command is not optimized through discord.py. This command takes a ridiculously long time.")

            global roles
            role = discord.utils.get(ctx.guild.roles, id=int(roles['party']))

            await ctx.trigger_typing()

            members = ""

            for member in ctx.guild.members:
                await ctx.trigger_typing()
                if role in member.roles:
                    members += f"{member.display_name}\n"
            

            embed = discord.Embed(
                color=discord.Color.blue(),
                title='Party Tag',
                description="All members searching for parties:\nhttps://hypixel.net/forums/bed-wars.138/"
            )

            embed.add_field(name=f"\uFEFF", value=members, inline=False)

            embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
            
            await ctx.send(embed=embed)

    @commands.command(name='previous_names', aliases=['nm', 'names'])
    async def previous_names(self, ctx, ign):
        await ctx.trigger_typing()


        uuid = API.get_uuid(self, ign)[0]

        names = API.get_names(self, uuid)

        embed = discord.Embed(
                color=discord.Color.green(),
                title='Previous Names for {}'.format(ign),
                description='https://namemc.com/profile/{}'.format(ign)
            )

        names_string = ''
        for i in range(len(names)-1):
            names_string += f'`{names[i]}`\n'
        
        embed.add_field(name=f"\uFEFF", value=f'{names_string}')

        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
            
        await ctx.send(embed=embed)

    @previous_names.error
    async def previous_names_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Name History **`ERROR`** | Names takes one argument: Username')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Name History **`ERROR`** | This might be an invalid username.')

    @commands.command(name="status")
    async def status(self, ctx, ign: str=None):
        await ctx.trigger_typing()

        if ign == None:
            ign = ctx.author.nick
            ign = Calcs.get_nick(self, ign)
            await ctx.send(f"using ign: {ign}")

        await ctx.trigger_typing()

        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            if hypixel_data["cause"] == 'Invalid API key':
                await ctx.send("Invalid API Key")
            
            await ctx.send(ctx.message.author.mention)
            await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before!'))

        online = False
        color = discord.Color.red()
        try:
            if int(hypixel_data['player']["lastLogin"]) > int(hypixel_data['player']["lastLogout"]):
                online = True
                color = discord.Color.green()
            else:
                pass
        except:
            online = 'UNKNOWN'

        image = f"https://mc-heads.net/head/{uuid}/128"
        image_full = f"https://mc-heads.net/body/{uuid}/512"

        embed = discord.Embed(
                title = "Status",
                description = "\uFEFF",
                color = color
        )
        embed.set_author(
            name = ign,
            icon_url = image
        )
        embed.set_image(url = image_full)

        try:
            embed.add_field(
            name="Prefix",
            value='`{}`'.format(hypixel_data['player']["prefix"])
            )
        except:
            pass
        embed.add_field(
            name="Rank",
            value=f'`{Calcs.Rank.rank(self, ign)}`'
            )
        embed.add_field(
            name="Level",
            #networkLevel = (sqrt((2 * hypixel_data['player']["networkExp"]) + 30625) / 50) - 2.5
            value='`{}`'.format(round(Calcs.get_hypixel_network_level(self, hypixel_data['player']["networkExp"])), 2)
            )
        embed.add_field(
            name="Karma",
            value='`{:,d}`'.format(hypixel_data['player']["karma"])
            )
        embed.add_field(
            name="Guild",
            value=f'`{API.get_guild(self, ign)}`'
            )
        embed.add_field(
            name="NameMC",
            value='https://namemc.com/profile/{}'.format(ign),
            inline=False
            )
        embed.add_field(
            name="\uFEFF",
            value='\uFEFF',
            inline=False
            )
        try:
            embed.add_field(
                name="Last Login",
                value=datetime.fromtimestamp(round(int(hypixel_data['player']["lastLogin"])/1000,0)),
                inline=False
                )
            embed.add_field(
                name="Last Logout",
                value=datetime.fromtimestamp(round(int(hypixel_data['player']["lastLogout"])/1000,0)),
                inline=False
                )
        except:
            pass
        embed.add_field(
            name="Online",
            value=f'`{online}`',
            inline=False
            )
        embed.add_field(
            name="Discord",
            value=f'`{Calcs.get_socials(self, ign)}`',
            inline=False
            )
        try:
            embed.add_field(name="Last Game Played", value='`{}`'.format(hypixel_data['player']["mostRecentGameType"]))
        except:
            embed.add_field(name="Last Game Played", value='`UNKNOWN`')

        await ctx.send(ctx.message.author.mention)
        return await ctx.send(embed=embed)

    @status.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
           await ctx.send('Status **`ERROR`** | Status takes one argument: Username')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Status **`ERROR`** | This might be an outdated or invalid username.')

    
    @commands.command(name="guild", aliases=['g'])
    async def guild(self, ctx, ign: str=None, guild_name: str=None, list_members: str=None):
        await ctx.trigger_typing()

        if ign == None:
            ign = ctx.author.nick
            ign = Calcs.get_nick(self, ign)
            await ctx.send(f"using ign: {ign}")

        if guild_name == None:
            guild_name = API.get_guild(self, ign)

        guild_data = None

        use_guild_name = False

        if ign == "info" and guild_name != None:
            await ctx.send(f'Getting guild info for "{guild_name}"')
            guild_data = API.get_guild(self, ign, guild_name)
            use_guild_name = True


        await ctx.trigger_typing()
        
        uuid = None

        show_data = False

        try:
            uuid = API.get_uuid(self, ign)[0]
        except:
            pass

        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            if hypixel_data["cause"] == 'Invalid API key':
                await ctx.send("Invalid API Key")
            
            await ctx.send(ctx.message.author.mention)
            await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before!'))

        creation_date = "?"
        level = "?"
        most_earnings_game = "?"
        owner = "?"

        try:
            if use_guild_name == False:
                guild_data = API.get_guild(self, ign, guild_name)

            creation_date = guild_data['guild']['created']
            creation_date = datetime.utcfromtimestamp(int(creation_date)/1000).strftime('%Y-%m-%d %H:%M:%S')
            level = Calcs.get_guild_level(int(guild_data['guild']['exp']))

            games = []
            game_earnings = []
            for game in guild_data['guild']['guildExpByGameType']:
                games.append(game)
                game_earnings.append(guild_data['guild']['guildExpByGameType'][game])
            max_earnings_index = game_earnings.index(max(game_earnings))
            most_earnings_game = games[max_earnings_index]

            for member in guild_data['guild']['members']:
                if member['rank'] == "Guild Master":
                    owner = API.get_ign(self, member['uuid'])

            show_data = True
        except:
            if guild_name == "?" or guild_name == None:
                guild_name = ""
            if ign == "info" and use_guild_name == True:
                ign = ""
            await ctx.send(f'The guild "{guild_name}" doesn\'t exist \nor the player "{ign}" does not belong to a guild.')



        color = discord.Color.blue()
        color2 = discord.Color.blurple()


        image = f"https://mc-heads.net/head/{uuid}/128"

        embed = discord.Embed(
                title = "Guild | {}".format(guild_name),
                description = "\uFEFF",
                color = color
        )
        if use_guild_name == False:
            embed.set_author(
                name = ign,
                icon_url = image
            )


        embed.add_field(
        name="Creation Date",
        value='`{}`'.format(creation_date),
        inline=False
        )
        embed.add_field(
        name="Guild Level",
        value='`{}`'.format(level)
        )
        embed.add_field(
        name="Owner",
        value='`{}`'.format(owner),
        )
        embed.add_field(
        name="Most Played Game",
        value='`{}`'.format(most_earnings_game)
        )

        if show_data == True:
            await ctx.send(ctx.message.author.mention)
            await ctx.send(embed=embed)

        if list_members == "members" or list_members != "":

            embed = discord.Embed(
                title = "Guild Members | {}".format(guild_name),
                description = "\uFEFF",
                color = color2
            )

            for member in guild_data['guild']['members']:
                member_ign = API.get_ign(self, member['uuid'])
                member_join_date = member['joined']
                member_join_date = datetime.utcfromtimestamp(int(member_join_date)/1000).strftime('%Y-%m-%d')
                member_rank = member['rank']

                embed.add_field(
                name=f"**{member_ign}**",
                value=f'''
                - joined on `{member_join_date}`
                - rank . . . . .`{member_rank}`
                ''',
                inline=False
                )

            return await ctx.send(embed=embed)

    #@guild.error
    async def guild_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
           await ctx.send('Guild **`ERROR`** | Status takes one argument: Username')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Guild **`ERROR`** | This might be an outdated or invalid username.')

def setup(bot):
    bot.add_cog(Party(bot))