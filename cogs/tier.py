import discord
from discord.ext import commands

import json
import math

from cogs.calcs import Calcs
from cogs.api import API

from cogs.admin import roles
from cogs.admin import tiers

class Tier(commands.Cog):
    def __init__(self, bot):
        # self.new_tn = NewTier()
        self.bot = bot
        
    @commands.command(name='bedwars', aliases=['bw'])
    async def bedwars(self, ctx, ign: str, mode_input: str='0'):
        await ctx.trigger_typing()
        
        uuid = API.get_uuid(self, ign)[0]

        #check username
        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            await ctx.send(ctx.message.author.mention)
            return await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before.'))

        image = f"https://mc-heads.net/head/{uuid}/128"
        image_full = f"https://mc-heads.net/body/{uuid}/128"

        mode_name = ''
        if mode_input == '0':
            mode_name == 'All'
        else:
            mode_name = mode_input

        #filter user to usable
        mode = 0
        mode_input = mode_input.lower()

        if mode_input == '0':
            mode = 0
        elif 'solo' in mode_input or '1' in mode_input:
            mode = 1
        elif 'duo' in mode_input or 'double' in mode_input or '2' in mode_input:
            mode = 2
        elif 'trio' in mode_input or 'triples' in mode_input or '3' in mode_input:
            mode = 3
        elif 'four' in mode_input or '4' in mode_input:
            mode = 4
        else:
            await ctx.send(f'Unable to interpret `{mode_input}`')

        embed = discord.Embed(
                title = f"{mode_name} Stats",
                description = "\uFEFF",
                colour = discord.Color.blue()
        )
        embed.set_author(
            name = ign,
            icon_url = image
        )

        stats = Calcs.get_bw(self, ign, mode)
        #[stars, fkdr_raw, fkdr, final_kills, final_deaths, kdr, kills, deaths, bblr, beds_broken, beds_lost, wlr, wins, losses, games_played, winstreak, resources]

        stats_set_names = ["Stars", "fkdr","FKDR","Final Kills","Final Deaths","KDR","Kills","Deaths","BBLR","Beds Broken","Beds Lost","WLR","Wins","Losses","Games Played","Winstreak", "Iron | Gold"]

        stars = stats[0]
        fkdr = stats[1]
        final_kills = stats[3]
        final_deaths = stats[4]
        kdr = stats[5]
        kills = stats[6]
        deaths = stats[7]
        bblr = stats[8]
        beds_broken = stats[9]
        beds_lost = stats[10]
        winrate = stats[11]
        wins = stats[12]
        losses = stats[13]
        games_played = stats[14]
        winstreak = stats[15]
        resources = stats[16]


        next_fkdr = math.ceil(fkdr)
        if next_fkdr == fkdr:
            next_fkdr += 1
        finals_reqd = round(next_fkdr * final_deaths - final_kills, 0)
        games_est = round((final_kills/games_played)*finals_reqd,0)
        
        embed.set_thumbnail(url = image_full)

        for i in range(len(stats_set_names)):
            if i == 2:
                continue
            if i == 3:
                embed.add_field(
                name=f"Finals Until {next_fkdr} FKDR | Predicted Games",
                value=f"`{finals_reqd} | {games_est}`",
                inline=False
                )
            value = stats[i]
            try:
                value = '{:,d}'.format(value)
            except:
                pass
            embed.add_field(
                name=stats_set_names[i],
                value=f'`{value}`',
                )

        embed.add_field(
                name="\uFEFF",
                value="\uFEFF",
                inline=False
                )
        embed.add_field(
            name="Rank",
            value=f'`{Calcs.Rank.rank(self, ign)}`'
            )


        await ctx.send(ctx.message.author.mention)
        return await ctx.send(embed=embed)

    @bedwars.error
    async def bedwars_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Bedwars Stats **`ERROR`** | This might be an outdated or invalid username.')

    @commands.command(name='skywars', aliases=['sw'])
    async def skywars(self, ctx, ign: str):
        await ctx.trigger_typing()
        
        uuid = API.get_uuid(self, ign)[0]

        #check username
        hypixel_data = API.get_hypixel(self, uuid)
        if not bool(hypixel_data["success"]):
            await ctx.send(ctx.message.author.mention)
            return await ctx.send(embed=discord.Embed(description = f'The player "{ign}" doesn\'t exist or has not logged on to Hypixel before.'))

        image = f"https://mc-heads.net/head/{uuid}/128"
        image_full = f"https://mc-heads.net/body/{uuid}/128"

        embed = discord.Embed(
                title = f"Skywars Stats",
                description = "\uFEFF",
                colour = discord.Color.purple()
        )
        embed.set_author(
            name = ign,
            icon_url = image
        )

        stats = Calcs.get_sw(self, ign)

        stats_set_names = ['Stars', 'KDR', 'Kills', 'Games Played', 'Wins', 'Winrate', 'Heads', 'Shards', 'Opals']
        #[stars, kdr, kills, games, winrate, heads, shards, opals]

        embed.set_thumbnail(url = image_full)
        
        for i in range(len(stats_set_names)):
            if i == 6:
                embed.add_field(
                name="\uFEFF",
                value="\uFEFF",
                inline=False
                )
            value = stats[i]
            try:
                value = '{:,d}'.format(value)
            except:
                pass
            embed.add_field(
                name=stats_set_names[i],
                value=f'`{value}`',
                )

        await ctx.send(ctx.message.author.mention)
        return await ctx.send(embed=embed)

    @skywars.error
    async def skywars_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Skywars Stats **`ERROR`** | This might be an outdated or invalid username.')

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

        #[stars, fkdr_raw, final_kills, kills, bblr, beds_broken, wlr, wins, games_played]
        set_names = ["Stars", "FKDR", "Final Kills", "Kills", "BBLR", "Beds Broken", "WLR", "Wins", "Games Played"]

        for i in range(len(set_names)):
            embed.add_field(
                name=set_names[i],
                value=f'`{str(closest_stat[0][i])}`',
                inline=True
            )

        await ctx.send(embed=embed)

    @closest_rank.error
    async def closest_rank_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Closest Rank **`ERROR`** | Are you inputting all arguments? Otherwise, I could not find that member.\n```\n<required> [optional]\n```\n```\nCommand Example:\n.cr <ign>\n```')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Closest Rank **`ERROR`** | Are you inputting all arguments? Otherwise, invalid username.\n```\n<required> [optional]\n```\n```\nCommand Example:\n.cr <ign>\n```')

    @commands.command(name='rank_difference', aliases=['rd'])
    async def rank_difference(self, ctx, ign: str, stat: str=None):
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

        stat_value_difference = Calcs.Get_Tier.get_next_difference(self, Calcs.get_nick(self, ign))

        if stat == None:

            embed = discord.Embed(
                    title = "Rank Difference",
                    description = "\uFEFF",
                    colour = discord.Color.orange()
            )
            embed.set_author(
                name = ign,
                icon_url = image
            )

            rel_val = float(stat_difference[2])
            abs_val = float(stat_difference[3])
            values = [rel_val, abs_val]

            for j in range(len(values)):
                if values[j] >= 1:
                    values[j] = f'+{round(abs(values[j]-1)*100)}%'
                elif values[j] < 1:
                    values[j] = f'-{round(abs(values[j]-1)*100)}%'

            embed.add_field(
                name="Overall Rank Difference",

                value=f'Relative | Overall\n`{values[0]}` | `{values[1]}`',
                )
            embed.add_field(
                name="\uFEFF",
                value='Difference from current to next nearest tier',
                inline=False
                )

            #[stars, fkdr_raw, final_kills, kills, bblr, beds_broken, wlr, wins, games_played]

            set_names = ["Stars", "FKDR", "Final Kills", "Kills", "BBLR", "Beds Broken", "WLR", "Wins", "Games Played"]

            for i in range(len(set_names)):
                
                rel_val = float(stat_difference[0][i])
                abs_val = float(stat_difference[1][i])
                values = [rel_val, abs_val]

                for j in range(len(values)):
                    if values[j] >= 1:
                        values[j] = f'+{round(abs(values[j]-1)*100)}%'
                    elif values[j] < 1:
                        values[j] = f'-{round(abs(values[j]-1)*100)}%'

                embed.add_field(
                    name=set_names[i],
                    value=f'`{values[0]} | {values[1]}`',
                    inline=True
                )

        else:
            await ctx.send(f"Interpreting \"{stat}\"...")
            await ctx.trigger_typing()

            # convert user input into usable index

            return_values = True

            stat_index = 0
           #tier difference [stars, fkdr_raw, final_kills, kills, bblr, beds_broken, wlr, wins, games_played]
            stat_index_names = ['Stars', 'FKDR', 'Final Kills', 'Kills', 'BBLR', 'Beds Broken', 'WLR', 'Wins', 'Games Played',]

            if "star" in stat.lower():
                stat_index = 0
            elif "fkdr" in stat.lower():
                stat_index = 1
            elif "final" in stat.lower():
                stat_index = 2
            elif "kill" in stat.lower():
                # kills input tested after finals in the case of 'final kills' input
                stat_index = 3
            elif "bblr" in stat.lower():
                stat_index = 4
            elif "bed" in stat.lower():
                stat_index = 5
            elif "wlr" in stat.lower():
                stat_index = 6
            elif "wins" in stat.lower():
                stat_index = 7
            elif "game" in stat.lower():
                stat_index = 8
            else:
                await ctx.send(f"Unable to interpret: \"{stat}\".")
                return_values = False

            stat_values = Calcs.get_bw(self, Calcs.get_nick(self, ign))
            abbv_list = [0,1,3,6,8,9,11,12,14]
            stats_list = []
            for i in range(len(abbv_list)):
                stats_list.append(stat_values[abbv_list[i]])
            closest_tier  = Calcs.Get_Tier.get_closest(self, Calcs.get_nick(self, ign))
            tier_values = Calcs.Get_Tier.__init__(self)

            embed = discord.Embed(
                    title = "Value to Next Rank",
                    description = "\uFEFF",
                    colour = discord.Color.dark_gold()
            )
            embed.set_author(
                name = ign,
                icon_url = image
            )
            if return_values == True:
                closest_tier_value = closest_tier[0][stat_index]
                print(tier_values[stat_index][closest_tier_value+1])
                print(stats_list[stat_index])
                
                tier_val = tier_values[stat_index][closest_tier_value+1]
                current_val = stats_list[stat_index]
                try:
                    current_val = float(current_val.strip('%'))
                except:
                    pass

                embed.add_field(
                    name=f"{stat_index_names[stat_index]} Value @ {closest_tier_value} | Amount Needed for Next Rank: {closest_tier_value+1}",
                    value=f'`{str(stats_list[stat_index])}` | `{str(round(tier_val - current_val,2))}`',
                    )


        await ctx.send(embed=embed)

    @rank_difference.error
    async def rank_difference_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Rank Difference **`ERROR`** | Are you inputting all arguments? Otherwise, I could not find that member.\n```\n<required> [optional]\n```\n```\nCommand Example:\n.rd <ign>\n```')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Rank Difference **`ERROR`** | Are you inputting all arguments? Otherwise, invalid username.\n```\n<required> [optional]\n```\n```\nCommand Example:\n.rd <ign>\n```')

    @commands.command(name='tier', aliases=['t'])
    #@commands.has_permissions(kick_members=True)
    async def tier(self, ctx, get: str=None, ign: str=None, member: discord.Member=None):
        await ctx.trigger_typing()

        global roles

        Calcs.Get_Tier.__init__(self)

        on_self = False
        if ign == None:
            ign = ctx.author.nick
            ign = Calcs.get_nick(self, ign)
            await ctx.send(f"using ign: {ign}")
            on_self = True

        if member == None:
            member = ctx.author

        await ctx.send(embed=discord.Embed(
            color=discord.Color.dark_red(),
            description="**`[!]`** This may take a moment"
        ))

        stat_difference = Calcs.Get_Tier.get_difference(self, Calcs.get_nick(self, ign))
        rel_val = float(stat_difference[2])
        abs_val = float(stat_difference[3])
        values = [rel_val, abs_val]

        for j in range(len(values)):
            if values[j] >= 1:
                values[j] = f'+{round(abs(values[j]-1)*100)}%'
            elif values[j] < 1:
                values[j] = f'-{round(abs(values[j]-1)*100)}%'
        closest_rank = Calcs.Get_Tier.get_closest(self, ign)[1]

        rank_roles = []
        role = roles['tier'][Calcs.Get_Tier.to_romans(self, int(closest_rank))]

        #fill potential rank roles with suffixes
        for i in range(6):
            rank_roles.append(str(Calcs.Get_Tier.to_romans(self, i)))

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"{ign}'s Tier\nNOTE: in the future, a ranking leaderboard will be featured for each tier!",
        )

        try:
            embed.add_field(name="Closest Tier", value=f"`{round(closest_rank)}`", inline=False)
            embed.add_field(name=f"Rank Difference", value=f'`Relative | Overall\n{values[0]}` | `{values[1]}`', inline=False)
            embed.add_field(name="Role:", value=f"`{str(Calcs.Get_Tier.to_romans(self, int(closest_rank)))}`")
        except:
            embed.add_field(name="Role:", value=f"`NONE`")

        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)
        
        if str(get).lower() == "y" or str(get).lower() == "yes":
            if ctx.message.author.guild_permissions.kick_members or on_self == True:
                await ctx.send(ctx.author.mention + f', assigning **{member.display_name}** `{str(Calcs.Get_Tier.to_romans(self, int(closest_rank)))}`!')

                for i in range(len(rank_roles)):
                    await member.remove_roles(discord.utils.get(member.guild.roles, name=rank_roles[i]))

                await member.add_roles(discord.utils.get(ctx.guild.roles, id=int(role)))
            else:
                await ctx.send(ctx.author.mention + f', you have insufficient permissions to assign this role.')
        else:
            pass

    @tier.error
    async def tier_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Tier **`ERROR`** | Are you inputting all arguments? Otherwise, I could not find that member.\n```\n<required> [optional]\n```\n```\nCommand Example:\n.t <yes|y - (any other single arg.)> [ign=self] [member=self]\n```')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Tier **`ERROR`** | Are you inputting all arguments? Otherwise, invalid username.\n```\n<required> [optional]\n```\n```\nCommand Example:\n.t <yes|y - (any other single arg.)> [ign=self] [member=self]\n```')
    
    
    i = 0
    # update nick w/ stars prefix
    @commands.Cog.listener()
    async def on_message(self, ctx):
        global roles
        i = Tier.i
        colors = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x0067FF, 0xB600FF]
        role = discord.utils.get(ctx.guild.roles, id=int(722237147972894771))
        if role in ctx.author.roles:
            i += 1
            i %= len(colors)
            try:
                await role.edit(colors[i])
            except:
                pass

        if not ctx.content.startswith('.') and ctx.author.bot == False:
            try:
                nick = ctx.author.display_name
                nick = Calcs.get_nick(self, nick)
                    
                stars = 0

                try:
                    stars = Calcs.get_bw(self, nick)[0]
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
    
    @commands.command(name='view_tier', aliases=['vt'])
    async def view_tier(self, ctx, level=0):
        await ctx.trigger_typing()
        
        global tiers
        embed = discord.Embed(
            color=discord.Color.greyple(),
            title="Tier Levels",
            description="Include an argument to view individual tiers",
        )

        tiers_keys = list(tiers.keys())
        tiers_values = []
        for i in range(len(tiers_keys)):
            tiers_values.append(tiers[str(tiers_keys[i])])
            for char in ['[',']']:
                tiers_values[i] = tiers_values[i].replace(char,'')
            tiers_values[i] = list(tiers_values[i].split(","))

        in_range = True

        try:
            level = int(level)
        except:
            await ctx.send(f'Unable to interpret tier: {level}')

        if level == 0:
            for i in range(len(tiers_keys)):
                embed.add_field(name=tiers_keys[i], value=str(tiers[str(tiers_keys[i])]).replace(",",", "), inline=False)
        elif level in range(1,len(tiers_values[0])): #arbitrary which stat is chosen, hopefully they are all the same length
            for i in range(len(tiers_keys)):
                embed.add_field(name=tiers_keys[i], value=str(tiers_values[i][level]).replace(",",", ").replace("'",""), inline=False)
        else:
            await ctx.send(f'Tier {level} out of range.')
            in_range = False

        
        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")

        if in_range == True:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tier(bot))