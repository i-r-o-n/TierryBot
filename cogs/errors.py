from discord.ext import commands
from discord.ext.commands.core import command

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Error | Missing Required Argument')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Error | Command Not Found')
        if isinstance(error, commands.BadArgument):
            await ctx.send('Error | Bad Argument')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Error | Command Invoke Error ... Check Console Logs for more Information')
        if isinstance(error, commands.ExtensionFailed):
            await ctx.send('Error | Extension Failed')

def setup(bot):
    bot.add_cog(Errors(bot))