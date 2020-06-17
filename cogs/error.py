from discord.ext import commands
from discord.ext.commands.core import command

class Error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Generic - **`ERROR`** | Missing Required Argument')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Generic - **`ERROR`** | Command Not Found')
        if isinstance(error, commands.BadArgument):
            await ctx.send('Generic - **`ERROR`** | Bad Argument')

def setup(bot):
    bot.add_cog(Error(bot))