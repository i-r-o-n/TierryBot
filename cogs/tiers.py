from cogs.calcs import Calcs
import discord
from discord.ext import commands
import os
from statistics import mean
import json

with open('secrets.json') as f:
    confidentials = json.load(f)

User = confidentials['User']


#Change Path to Directory
os.chdir(f'c:\\Users\\{User}\\desktop\\bot')

tier_roles = (
    'Tier I',
    'Tier II',
    'Tier III',
    'Tier IV',
    'Tier V',
    'Tier VI',
    'Tier VII'
)

star_roles = (
    '[100✫]',
    '[200✫]',
    '[300✫]',
    '[400✫]',
    '[500✫]',
    '[600✫]',
    '[700✫]',
    '[800✫]',
    '[900✫]',
    '[1000✫]'
)

class Tiers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info', aliases=['in','i','stat'])
    async def info(self, ctx, ign):
        async with ctx.typing():
            await ctx.send(embed=discord.Embed(
                color=discord.Color.dark_red(),
                description="This may take a moment"
            ))

        embed = discord.Embed(
            color=discord.Color.purple(),
            description=f"{ign}'s Tier info",
        )

        embed.add_field(name="Closest Tier", value=(int(Calcs.ClosestRank(self, ign)[1])), inline=False)
        embed.add_field(name=f"Mean Difference between {ign}'s Stats & Closest Tier requirements:", value=(mean(Calcs.Difference(self, ign)[1])), inline=False)
        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

    @commands.command(name='star',aliases=['s'])
    @commands.has_permissions(kick_members=True)
    async def star(self, ctx, ign: str=None, member: discord.Member=None):
        log = open("log.txt","a")
        
        global star_roles
        
        if ign == None:
            ign = ctx.author.nick
            await ctx.send(f"using ign: {ign}")

        if member == None:
            member = ctx.author

        async with ctx.typing():
            await ctx.send(embed=discord.Embed(
                color=discord.Color.dark_red(),
                description="This may take a moment"
            ))

        ign_star = round(Calcs.StarsfromXP(self, ign),0)
        star = 0
        while ign_star > 100:
            ign_star -= 100
            star += 100

        for i in range(len(star_roles)):
            star_role = discord.utils.get(ctx.guild.roles, name=str(star_roles[i]))
            await member.remove_roles(star_role)

        role = discord.utils.get(ctx.guild.roles, name=f"[{star}✫]")
        star_colors = [0, 0xfefefe, 0xffaa00, 0x00ffff, 0x008800, 0x008888, 0x920000, 0xff00ff, 0x0a0aff, 0xb000ff, 0x000000]

        embed = discord.Embed(
            color=discord.Color(star_colors[int(star/100)]),
            description=f"{ign}'s Stars",
            )

        embed.add_field(name="Star rank:", value=role)
        embed.add_field(name="Stars", value=f"{round(Calcs.StarsfromXP(self, ign),1)}✫")
        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

        await member.add_roles(role)

        log.write(f"\nS, {member}, {star}")
        log.close()        

    @commands.command(name='tier', aliases=['t'])
    @commands.has_permissions(kick_members=True)
    async def tier(self, ctx, ign: str=None, member: discord.Member=None):
        log = open("log.txt","a")

        global tier_roles

        if ign == None:
            ign = ctx.author.nick
            await ctx.send(f"using ign: {ign}")

        if member == None:
            member = ctx.author

        async with ctx.typing():
            await ctx.send(embed=discord.Embed(
                color=discord.Color.dark_red(),
                description="This may take a moment"
            ))

        role = discord.utils.get(ctx.guild.roles, name=str(Calcs.GetRole(self, int(Calcs.ClosestRank(self, ign)[1]))))

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"{ign}'s Tier info\nNOTE: in the future -> a ranking system will be featured for each tier",
        )

        embed.add_field(name="Closest Tier", value=(int(Calcs.ClosestRank(self, ign)[1])), inline=False)
        embed.add_field(name=f"Mean Difference between {ign}'s Stats & Closest Tier requirements:", value=(round(mean(Calcs.Difference(self, ign)[1]),2)), inline=False)
        embed.add_field(name="Role:", value=role)
        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

        for i in range(len(tier_roles)):
            await member.remove_roles(discord.utils.get(member.guild.roles, name=tier_roles[i]))

        await member.add_roles(role)

        log.write(f"\nR, {member}, {role}")
        log.close()

    @commands.command(name='tier members', aliases=['tm'])
    async def tier_members(self, ctx, role: discord.Role=None):
        pass


def setup(bot):
    bot.add_cog(Tiers(bot))