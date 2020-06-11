import discord
from discord.ext import commands
import requests
#from cogs.calcs import hypixel_key
from cogs.calcs import hypixel_key
import json

with open('secrets.json') as f:
    confidentials = json.load(f)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def RetrieveRank(self, ign):
        data = requests.get(f"https://api.hypixel.net/player?key={hypixel_key}&name={ign}").json()
        try:
            return data["player"]["newPackageRank"] #if ["newPackageRank"] in ['newPackageRank']["player"] else 0
        except:
            return 0
        
    def RetrieveSubscriptionStatus(self, ign):
        data = requests.get(f"https://api.hypixel.net/player?key={hypixel_key}&name={ign}").json()
        #return data["player"]["monthlyPackageRank"] if "monthlyPackageRank" in data["player"] else 0
        return 1 if "monthlyPackageRank" in data["player"] else 0

    @commands.command(name='ping', aliases=['p'])
    @commands.guild_only()
    async def ping(self, ctx):
        ms = (f'Pong! {round(self.bot.latency * 1000)}ms')
        embed = discord.Embed(
            color=discord.Color.blurple(),
            description=ms
        )
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

    @commands.command(name='info', aliases=['botinfo'])
    @commands.guild_only()
    async def general_info(self, ctx):
        info = (f'Proprietary Bot')
        embed = discord.Embed(
            color=discord.Color.blurple(),
            description=info
        )
        await ctx.trigger_typing()
        await ctx.send(embed=embed)


    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, color=member.color)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)

    @commands.command(name='server icon', aliases=['si'])
    async def server_icon(self, ctx):
        embed = discord.Embed(
            color=discord.Color.lighter_grey(),
            description='test'
        )
        embed.set_image(url=ctx.guild.icon)
        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

    @commands.command(name='verify',aliases=['v'])
    async def verify(self, ctx, ign: str=None, member: discord.Member=None):
        log = open("log.txt","a")

        if ign == None:
            ign = ctx.author.nick
            await ctx.send(f"using ign: {ign}")

        if member == None:
            member = ctx.author

        role = discord.utils.get(ctx.guild.roles, id=698403490086518794)
        #test server role id: 699089356501286923

        rank = General.RetrieveRank(self, ign)
        #rank role ids
        rank_role = 661937723501969410

        if rank == 'VIP':
            rank_role = 661937723136933889
        elif rank == 'VIP_PLUS':
            rank_role = 661937723099185165
        elif rank == 'MVP':
            rank_role = 661937722545537033
        elif rank == 'MVP_PLUS':
            rank_role = 661937722403061769
        else:
            pass

        rank_role = discord.utils.get(ctx.guild.roles, id=rank_role)

        if General.RetrieveSubscriptionStatus(self, ign) == 1:
            sub_role = discord.utils.get(ctx.guild.roles, id=661937722029768714)
            await member.add_roles(sub_role)
        else:
            pass

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"Verified: {ign}\n{role} {General.RetrieveRank(self, ign)}",
        )

        await ctx.trigger_typing()
        await ctx.send(embed=embed)

        await member.add_roles(role)
        await member.add_roles(rank_role)
        #NOTE bot cannot change nick of admins
        await member.edit(nick=ign)

        log.write(f"\nV, {member}, {ign}")
        log.close()

    @verify.error
    async def verify_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Do you have **ADMIN** permissions?\nCannot change nicknames of **ADMIN** users')

def setup(bot):
    bot.add_cog(General(bot))