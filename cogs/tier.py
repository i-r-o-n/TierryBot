import discord
from discord.ext import commands

import json

from cogs.calcs import Calcs
from cogs.api import API

from cogs.admin import roles

class Tier(commands.Cog):
    def __init__(self, bot):
        # self.new_tn = NewTier()
        self.bot = bot
        
    @commands.command(name='stats', aliases=['st'])
    async def stats(self, ctx, ign):
        await ctx.trigger_typing()
        
        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            await ctx.send(ctx.message.author.mention)
            return await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before.'))

        image = f"https://mc-heads.net/head/{uuid}/128"
        image_full = f"https://mc-heads.net/body/{uuid}/128"

        embed = discord.Embed(
                title = "Stats",
                description = "\uFEFF",
                colour = discord.Color.blue()
        )
        embed.set_author(
            name = ign,
            icon_url = image
        )

        embed.set_thumbnail(url = image_full)
        embed.add_field(
            name="Stars",
            value=f'`{Calcs.get_stats(self, ign)[0]}`',
            inline=True
            )
        embed.add_field(
            name="FKDR | Finals / Final Deaths",
            value=f'`{Calcs.get_stats(self, ign)[1]}`',
            inline=True
            )
        embed.add_field(
            name="Kills",
            value=f'`{Calcs.get_stats(self, ign)[2]}`',
            inline=True
            )
        embed.add_field(
            name="Games Played",
            value=f'`{Calcs.get_stats(self, ign)[5]}`',
            inline=True
            )
        embed.add_field(
            name="Beds Broken",
            value=f'`{Calcs.get_stats(self, ign)[6]}`',
            inline=True
            )

        embed.add_field(
            name="Winrate",
            value=f'`{Calcs.get_stats(self, ign)[3]}`',
            inline=False
            )
        embed.add_field(
            name="Winstreak",
            value=f'`{Calcs.get_stats(self, ign)[4]}`',
            inline=False
            )
    
        embed.add_field(
            name="\uFEFF",
            value='\uFEFF',
            inline=False
            )
        embed.add_field(
            name="Rank",
            value=f'`{Calcs.Rank.rank(self, ign)}`'
            )

        await ctx.send(ctx.message.author.mention)
        return await ctx.send(embed=embed)

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Stats **`ERROR`** | This might be an outdated or invalid username.')

    @commands.command(name='closest_rank', aliases=['cr'])
    async def closest_rank(self, ctx, ign):
        await ctx.trigger_typing()

        if ign == None:
            ign = ctx.author.nick
            ign = Calcs.get_nick(self, ign)
            await ctx.send(f"using ign: {ign}")
        
        Calcs.Get_Tier.__init__(self)

        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            await ctx.send(ctx.message.author.mention)
            return await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before.'))

        image = f"https://mc-heads.net/head/{uuid}/128"
        image_full = f"https://mc-heads.net/body/{uuid}/128"

        closest_stat = Calcs.Get_Tier.get_closest(self, Calcs.get_nick(self, ign))

        embed = discord.Embed(
                title = "Closest Rank",
                description = "\uFEFF",
                colour = discord.Color.teal()
        )
        embed.set_author(
            name = ign,
            icon_url = image
        )
        embed.add_field(
            name="Overall Closest Rank",
            value=f'`{str(closest_stat[1])}`',
            # value = f'`{str(self.new_tn.get_closest(self, Calcs.get_nick(self, ign))[0][1])}`',
            )
        embed.add_field(
            name="\uFEFF",
            value='\uFEFF',
            inline=False
            )

        embed.set_thumbnail(url = image_full)
        embed.add_field(
            name="Stars",
            value=f'`{str(closest_stat[0][0])}`',
            inline=True
            )
        embed.add_field(
            name="FKDR",
            value=f'`{str(closest_stat[0][1])}`',
            inline=True
            )
        embed.add_field(
            name="Finals",
            value=f'`{str(closest_stat[0][2])}`',
            inline=True
            )
        embed.add_field(
            name="Kills",
            value=f'`{str(closest_stat[0][3])}`',
            inline=True
            )
        embed.add_field(
            name="Beds",
            value=f'`{str(closest_stat[0][4])}`',
            inline=True
            )
        embed.add_field(
            name="Games",
            value=f'`{str(closest_stat[0][5])}`',
            inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name='rank_difference', aliases=['rd'])
    async def rank_difference(self, ctx, ign):
        await ctx.trigger_typing()

        if ign == None:
            ign = ctx.author.nick
            ign = Calcs.get_nick(self, ign)
            await ctx.send(f"using ign: {ign}")
        
        Calcs.Get_Tier.__init__(self)

        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            await ctx.send(ctx.message.author.mention)
            return await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before.'))

        image = f"https://mc-heads.net/head/{uuid}/128"
        image_full = f"https://mc-heads.net/body/{uuid}/128"

        stat_difference = Calcs.Get_Tier.get_difference(self, Calcs.get_nick(self, ign))

        embed = discord.Embed(
                title = "Rank Difference",
                description = "\uFEFF",
                colour = discord.Color.orange()
        )
        embed.set_author(
            name = ign,
            icon_url = image
        )
        embed.add_field(
            name="Overall Rank Difference\nrelative | overall",
            value=f'`{str(stat_difference[1])}` | `{str(stat_difference[2])}`',
            )
        embed.add_field(
            name="\uFEFF",
            value='\uFEFF',
            inline=False
            )

        embed.set_thumbnail(url = image_full)
        embed.add_field(
            name="Stars\nrelative | overall",
            value=f'`{str(stat_difference[0][0])}` | `{str(stat_difference[0][6])}`',
            inline=True
            )
        embed.add_field(
            name="FKDR\nrelative | overall",
            value=f'`{str(stat_difference[0][1])}` | `{str(stat_difference[0][7])}`',
            inline=True
            )
        embed.add_field(
            name="Finals\nrelative | overall",
            value=f'`{str(stat_difference[0][2])}` | `{str(stat_difference[0][8])}`',
            inline=True
            )
        embed.add_field(
            name="Kills\nrelative | overall",
            value=f'`{str(stat_difference[0][3])}` | `{str(stat_difference[0][9])}`',
            inline=True
            )
        embed.add_field(
            name="Beds\nrelative | overall",
            value=f'`{str(stat_difference[0][4])}` | `{str(stat_difference[0][10])}`',
            inline=True
            )
        embed.add_field(
            name="Games",
            value=f'`{str(stat_difference[0][5])}` | `{str(stat_difference[0][11])}`',
            inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name='tier', aliases=['t'])
    #@commands.has_permissions(kick_members=True)
    async def tier(self, ctx, ign: str=None, member: discord.Member=None, get: str=None):
        await ctx.trigger_typing()

        global roles

        Calcs.Get_Tier.__init__(self)

        if ign == None:
            ign = ctx.author.nick
            ign = Calcs.get_nick(self, ign)
            await ctx.send(f"using ign: {ign}")

        if member == None:
            member = ctx.author


        await ctx.send(embed=discord.Embed(
            color=discord.Color.dark_red(),
            description="**`[!]`** This may take a moment"
        ))

        stat_difference = Calcs.Get_Tier.get_difference(self, Calcs.get_nick(self, ign))
        closest_rank = Calcs.Get_Tier.get_closest(self, ign)[1]

        rank_roles = []
        role = roles['tier'][Calcs.Get_Tier.to_romans(self, int(closest_rank))]

        if closest_rank != 0:
            for i in range(6):
                rank_roles.append(str(Calcs.Get_Tier.to_romans(self, i)))

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"{ign}'s Tier\nNOTE: in the future, a ranking system will be featured for each tier",
        )

        try:
            embed.add_field(name="Closest Tier", value=f"`{closest_rank}`", inline=False)
            embed.add_field(name=f"Rank Difference\nrelative | overall", value=f'`{str(stat_difference[1])}` | `{str(stat_difference[2])}`', inline=False)
            embed.add_field(name="Role:", value=f"`{str(Calcs.Get_Tier.to_romans(self, int(closest_rank)))}`")
        except:
            embed.add_field(name="Role:", value=f"`NONE`")

        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)
        
        if str(get).lower() == "y" or str(get).lower() == "yes":
            if ctx.message.author.guild_permissions.kick_members:
                await ctx.send(ctx.author.mention + f', assigning you `{str(Calcs.Get_Tier.to_romans(self, int(closest_rank)))}`!')
                for i in range(len(rank_roles)):
                    await member.remove_roles(discord.utils.get(member.guild.roles, name=rank_roles[i]))

                await member.add_roles(discord.utils.get(ctx.guild.roles, id=int(role)))
            else:
                await ctx.send(ctx.author.mention + f', you have insufficient permissions to assign this role.')
        else:
            pass

    # update nick w/ stars prefix
    @commands.Cog.listener()
    async def on_message(self, ctx):
        global roles

        if not ctx.content.startswith('.') and ctx.author.bot == False:
            try:
                nick = ctx.author.display_name
                nick = Calcs.get_nick(self, nick)
                    
                stars = 0

                try:
                    stars = Calcs.get_stats(self, nick)[0]
                except:
                    stars = '?'

                try:
                    await ctx.author.edit(nick=f'[{stars}✫] {nick}')
                except:
                    pass
                        
                rounded_star = 0
                try:
                    while int(stars) >= 100:
                        stars -= 100
                        rounded_star += 100
                except:
                    pass

                role = discord.utils.get(ctx.guild.roles, id=int(roles['star'][f'[{rounded_star}]']))
                await ctx.author.add_roles(role)

            except discord.errors.Forbidden:
                # Cannot change nick of admins
                pass

    


def setup(bot):
    bot.add_cog(Tier(bot))