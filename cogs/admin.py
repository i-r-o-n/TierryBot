import discord
from discord.ext import commands

import datetime
import json

# a json file is used for api keys and tokens.
with open('secrets.json') as f:
    secrets = json.load(f)

class Key:
    global secrets

    hypixel_key = secrets['Hypixel API Key']
    key_index_len = len(hypixel_key.keys())

    def get_key(self, index:int, hypixel_key=hypixel_key) -> str:
        hypixel_key = hypixel_key[str(index)]
        return hypixel_key

token = secrets['Discord Bot Token']


with open('roles.json') as f:
    roles = json.load(f)

with open('tiers.json') as f:
    tiers = json.load(f)


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # if ctx.author.server_permission.administrator:

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):

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

    @commands.command(name='kill', hidden=True)
    @commands.has_permissions(administrator=True)
    async def kill(self, ctx):
        await ctx.send(f"[{datetime.datetime.now()}] Shutting Down command from {ctx.author}\n")
        await ctx.send("shutting down...")
        return await ctx.bot.logout()

def setup(bot):
    bot.add_cog(Admin(bot))