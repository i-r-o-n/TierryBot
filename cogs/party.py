import discord
from discord.ext import commands


class Party(commands.Cog):

    @commands.command(name='party', aliases=['pl'])
    async def party_list(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=662429332186202123)

        embed = discord.Embed(
            color=discord.Color.blue(),
            title='Party Tag',
            description="All members searching for parties:"
        )

        for member in ctx.guild.members:
            if role in member.roles:
                embed.add_field(name=member.nick, value=f"{member}", inline=False)

        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Party(bot))