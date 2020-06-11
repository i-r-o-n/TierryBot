from discord.ext import commands
import json

#a json file is used for api keys and tokens.
with open('secrets.json') as f:
    confidentials = json.load(f)

hypixel_key = confidentials['Hypixel Key']

with open('secrets.json') as f:
    TOKEN = json.load(f)

TOKEN = TOKEN['TOKEN']

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # if ctx.author.server_permission.administrator:

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        if cog[0:5] == 'cogs.':
            cog = cog[5:len(cog)]
        else:
            pass

        try:
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.admin"""

        if cog[0:5] == 'cogs.':
            cog = cog[5:len(cog)]
        else:
            pass

        try:
            self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.has_permissions(administrator=True)
    async def reload_cog(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.admin"""
        log = open("admin_log.txt","a")
        
        if cog[0:5] == 'cogs.':
            cog = cog[5:len(cog)]
        else:
            pass

        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

        log.write(f"\nR, {cog}")
        log.close()


def setup(bot):
    bot.add_cog(Admin(bot))