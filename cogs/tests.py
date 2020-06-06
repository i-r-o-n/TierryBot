from cogs.calcs import Calcs
import discord
from discord.ext import commands


class TestsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test2')
    async def test1(self, ctx, ign):
        if ign is None:
            await ctx.send("IGN is required param")
        await ctx.trigger_typing()
        await ctx.send("This may take a moment...\nClosest Tier")
        await ctx.trigger_typing()
        await ctx.send('[star, kills, fkdr, finals, games, beds], rounded average')
        async with ctx.typing():
            await ctx.send(Calcs.ClosestRank(self, ign))

    @commands.command(name='test1')
    async def test2(self, ctx, ign):
        if ign is None:
            await ctx.send("IGN is required param")
        await ctx.trigger_typing()
        await ctx.send("This may take a moment...\nDifference in Player Stat and Tier Value")
        await ctx.trigger_typing()
        await ctx.send('[star, kills, fkdr, finals, games, beds]')
        async with ctx.typing():
            await ctx.send(Calcs.Difference(self, ign))

    @commands.command(name='test3')
    async def test3(self, ctx):
        
        embed = discord.Embed(
            color=discord.Color.blue(),
            title="Test Title",
            description="This is a test"
        )

        embed.set_author(name="Author", icon_url="https://img.icons8.com/ios-filled/100/000000/circled-t.png")
        embed.set_image(url="https://i.dlpng.com/static/png/6370277_preview.png")
        embed.set_thumbnail(url="https://i.dlpng.com/static/png/6370277_preview.png")
        embed.add_field(name="ping", value="This is a latentcy test", inline=False)
        embed.add_field(name="Test Field", value="this is a test", inline=False)
        embed.set_footer(text="this is a footer")

        await ctx.send(embed=embed)

    @commands.command(name='test4')
    async def test4(self, ctx, member: discord.Member, role):
        await ctx.send("adding roles")
        role = discord.utils.get(member.guild.roles, name="[100✫]")
        await member.add_roles(role)

    @commands.command(name='test5')
    async def test5(self, ctx, member: discord.Member):
        await member.edit(nick="test")

    @commands.command(name='test6')
    async def test6(self, ctx, ign: str=None):
        if ign == None:
            ign = ctx.author.nick
            await ctx.send(f"using ign: {ign}")
        else:
            await ctx.send(f"using set ign: {ign}")


def setup(bot):
    bot.add_cog(TestsCog(bot))