import discord
from discord.ext import commands

import json

from cogs.admin import roles
from cogs.calcs import Calcs
from cogs.api import API

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


    @commands.command(name='verify', aliases=['v'])
    async def verify(self, ctx, ign: str=None, member: discord.Member=None):
        await ctx.trigger_typing()

        global roles

        if ign == None:
            ign = ctx.author.nick
            ign = Calcs.get_nick(self, ign)
            await ctx.send(f"using ign: {ign}")

        if member == None:
            member = ctx.author


        v_role = discord.utils.get(ctx.guild.roles, id=int(roles['verify']))
        rank = str(Calcs.Rank.rank(self, ign).lower())
        
        rank_role = None

        try:
            rank_role = int(roles[rank])
        except:
            rank_role = int(roles['member'])

        rank_role = discord.utils.get(ctx.guild.roles, id=rank_role)

        if Calcs.Rank.get_sub(self, ign) == 1:
            sub_role = discord.utils.get(ctx.guild.roles, id=int(roles['mvp++']))
            await member.add_roles(sub_role)
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=int(roles['mvp+'])))
        else:
            pass

        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"Verified: {ign}\n{v_role} {rank}",
        )

        await member.add_roles(v_role)
        await member.add_roles(rank_role)
        #NOTE bot cannot change nick of admins
        await member.edit(nick=ign)

        await ctx.send(embed=embed)

    @verify.error
    async def verify_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Verify **`ERROR`** | I could not find that member...')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Verify **`ERROR`** | \nDo you have **ADMIN** permissions?\nCannot change nicknames of **ADMIN** users\nOtherwise, invalid username')
    
    @commands.command(name='send', aliases=['s'], hidden=True)
    async def send(self, ctx, keys:list, values:list, title):
        await ctx.trigger_typing()

        if type(keys) != list:
            keys = json.loads(keys)

        if type(values) != list:
            values = json.loads(values)

        embed = discord.Embed(
                title = title,
                description = "\uFEFF",
                colour = discord.Color.greyple()
        )
        for i in range(len(keys)):
            if keys[i] == ' ':
                embed.add_field(
                    name="\uFEFF",
                    value='\uFEFF',
                    inline=False
                    )
            else:
                embed.add_field(
                name=keys[i],
                value=f'`{values[i]}`',
                )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))