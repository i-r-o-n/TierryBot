import discord
from discord.ext import commands

import json

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

        embed = discord.Embed(
                title = f"{mode_input} Stats",
                description = "\uFEFF",
                colour = discord.Color.blue()
        )
        embed.set_author(
            name = ign,
            icon_url = image
        )

        stats = Calcs.get_bw(self, ign)

        fkdr = stats[1]
        finals = stats[2]

        next_fkdr = 1
        while fkdr >= 1:
            fkdr -= 1
            next_fkdr += 1

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
            pass


        finals_reqd = round(next_fkdr*(stats[2]/stats[1]) - finals, 0)
        
        if mode == 0:
            embed.set_thumbnail(url = image_full)
            embed.add_field(
                name="Stars",
                value=f'`{stats[0]}`',
                inline=True
                )
            embed.add_field(
                name="FKDR | Finals / Final Deaths",
                value=f'`{stats[8]}`',
                inline=True
                )
            embed.add_field(
                name="Finals until next FKDR | Projected Games to Achieve",
                # [stars, fkdr_raw, final_kills, kills, beds, games, winrate, winstreak, fkdr]
                value=f'`{int(finals_reqd)}` | `{int(round(finals_reqd/((stats[1]+next_fkdr)/2),1))}`',
                inline=True
                )
            embed.add_field(
                name="Kills",
                value=f'`{stats[3]}`',
                inline=True
                )
            embed.add_field(
                name="Beds Broken",
                value=f'`{stats[4]}`',
                inline=True
                )
            embed.add_field(
                name="Games Played",
                value=f'`{stats[5]}`',
                inline=True
                )

            embed.add_field(
                name="Winrate",
                value=f'`{stats[6]}`',
                inline=False
                )
            embed.add_field(
                name="Winstreak",
                value=f'`{stats[7]}`',
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
        elif mode in range(1,5):

            bedwars_stats = hypixel_data['player']['stats']['Bedwars']
            # ease of access list for api key names
            index_names = ['','eight_one_', 'eight_two_', 'four_three_', 'four_four_']
            chosen_index = '?'

            for i in range(1,5):
                if mode == i:
                    chosen_index = index_names[i]

            # set fallbacks for cross-mode stats
            m_fkdr = ['final_kills_bedwars', 'final_deaths_bedwars']
            m_kills = 'kills_bedwars'
            m_beds = 'beds_broken_bedwars'
            m_games = 'games_played_bedwars'
            m_winrate = ['wins_bedwars', 'losses_bedwars']
            m_resources = 'resources_collected_bedwars'

            try:
                m_fkills = bedwars_stats[str(chosen_index + m_fkdr[0])]
                m_fdeaths = bedwars_stats[str(chosen_index + m_fkdr[1])]
                m_fkdr = f'{round(m_fkills/m_fdeaths,2)} ({m_fkills}/{m_fdeaths})'
                m_kills = bedwars_stats[str(chosen_index + m_kills)]
                m_beds = bedwars_stats[str(chosen_index + m_beds)]
                m_games = bedwars_stats[str(chosen_index + m_games)]
                m_winrate = f'{round(bedwars_stats[str(chosen_index + m_winrate[0])]/m_games*100,2)}%'
                m_resources = f'{bedwars_stats[chosen_index + "iron_" + m_resources]} | {bedwars_stats[chosen_index + "gold_" + m_resources]}'
            except:
                pass
            


            embed.set_thumbnail(url = image_full)
            embed.add_field(
                name="Stars",
                value=f'`{stats[0]}`',
                inline=False
                )
            embed.add_field(
                name="FKDR | Finals / Final Deaths",
                value=f'`{m_fkdr}`',
                inline=True
                )
            embed.add_field(
                name="Kills",
                value=f'`{m_kills}`',
                inline=True
                )
            embed.add_field(
                name="Beds Broken",
                value=f'`{m_beds}`',
                inline=True
                )
            embed.add_field(
                name="Games Played",
                value=f'`{m_games}`',
                inline=True
                )
            embed.add_field(
                name="Winrate",
                value=f'`{m_winrate}`',
                inline=False
                )
            embed.add_field(
                name="Iron | Gold",
                value=f'`{m_resources}`',
                inline=False
                )
        else:
            await ctx.send(f'Unable to interpret `{mode_input}`')

        await ctx.send(ctx.message.author.mention)
        return await ctx.send(embed=embed)

    @bedwars.error
    async def bedwars_error(self, ctx, error):
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

        names = ["Stars", "FKDR", "Finals", "Kills", "Beds", "Games"]

        for i in range(len(names)):
            embed.add_field(
                name=names[i],
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

        else:
            await ctx.send(f"Interpreting \"{stat}\"...")
            await ctx.trigger_typing()

            # convert user input into usable index

            return_values = True

            stat_index = 0
            # Stats function: return [stars, fkdr_raw, final_kills, kills, beds, games, winrate, winstreak, fkdr]
            stat_index_names = ['Stars', 'FKDR', 'Final Kills', 'Kills', 'Beds', 'Games', 'Winrate', 'Winstreak', 'Final Kills / Deaths']
            # Stats value difference function: [star, fkdr, finals, kills, beds, games]

            if "star" in stat.lower():
                stat_index = 0
            elif "fkdr" in stat.lower():
                stat_index = 1
            elif "final" in stat.lower():
                stat_index = 2
            elif "kill" in stat.lower():
                # kills input tested after finals in the case of 'final kills' input
                stat_index = 3
            elif "bed" in stat.lower():
                stat_index = 4
            elif "game" in stat.lower():
                stat_index = 5
            else:
                await ctx.send(f"Unable to interpret: \"{stat}\".")
                return_values = False

            stat_values = Calcs.get_bw(self, Calcs.get_nick(self, ign))
            closest_tier  = Calcs.Get_Tier.get_closest(self, Calcs.get_nick(self, ign))

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
                embed.add_field(
                    name=f"{stat_index_names[stat_index]} Value @ {closest_tier_value} | Amount Needed for Next Rank: {closest_tier_value+1}",
                    value=f'`{str(stat_values[stat_index])}` | `{str(stat_value_difference[stat_index])}`',
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
        elif level in range(1,8):
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