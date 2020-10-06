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
                description="\uFEFF"
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
    async def status(self, ctx, ign):
        await ctx.trigger_typing()

        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            if hypixel_data["cause"] == 'Invalid API key':
                await ctx.send("Invalid API Key")
            
            await ctx.send(ctx.message.author.mention)
            return await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before!'))

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

def setup(bot):
    bot.add_cog(Party(bot))