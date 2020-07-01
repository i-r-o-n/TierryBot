import discord
from discord.ext import commands

import datetime
import json

# a json file is used for api keys and tokens.
with open('secrets.json') as f:
    secrets = json.load(f)

token = secrets['Discord Bot Token']


class Key:
    global secrets

    hypixel_key = secrets['Hypixel API Key']
    key_index_len = len(hypixel_key.keys())

    def get_key(self, index:int, hypixel_key=hypixel_key) -> str:
        hypixel_key = hypixel_key[str(index)]
        return hypixel_key


with open('roles.json') as f:
    roles = json.load(f)

with open('tiers.json') as f:
    tiers = json.load(f)

from cogs.api import API

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # if ctx.author.server_permission.administrator:

    @commands.command(name='get_keys', hidden=True, aliases=['gk'])
    @commands.is_owner()
    async def get_keys(self, ctx):

        for i in range(Key.key_index_len):
            key = Key.hypixel_key[str(i)]
            key_info = API.get_key_info(self, key)

            if key_info[0] != False:
                owner = str(key_info[1]).replace('-','')

                embed = discord.Embed(
                    title = "Hypixel API Keys Status",
                    description = "\uFEFF",
                    colour = discord.Color.green()
                )
                embed.set_author(
                    name = '[!] Confidential'
                )
                embed.add_field(
                    name=f"{API.get_ign(self, owner)}",
                    value=f'`{key_info[0]}`'
                    )


                embed.add_field(
                    name=f"Queries: Total",
                    value=f'`{key_info[2]}`'
                    )
                embed.add_field(
                    name=f"Queries: Past Min",
                    value=f'`{key_info[3]}`'
                    )
                embed.add_field(
                    name=f"Queries: Limit",
                    value=f'`{key_info[4]}`'
                    )

                embed.add_field(
                    name=f"\uFEFF",
                    value=f'\uFEFF',
                    inline=False
                    )

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title = "Hypixel API Keys Status",
                    description = "\uFEFF",
                    colour = discord.Color.red()
                )
                embed.set_author(
                    name = '[!] Error'
                )
                embed.add_field(
                    name=f"**`ALERT!`** | `{key_info[1]}`",
                    value=f'`{key_info[2]}`'
                    )

                await ctx.send(embed=embed)

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