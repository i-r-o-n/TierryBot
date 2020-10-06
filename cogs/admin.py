import discord
from discord.ext import commands

import datetime
import json

# a json file is used for api keys and tokens.
with open('secrets.json') as f0:
    secrets = json.load(f0)

token = secrets['Discord Bot Token']

with open('roles.json') as f1:
    roles = json.load(f1)

with open('tiers.json') as f2:
    tiers = json.load(f2)

class Key:
    global secrets

    hypixel_key = secrets['Hypixel API Keys']
    key_index_len = len(hypixel_key.keys())

    def get_key(self, index:int, hypixel_key=hypixel_key) -> str:
        hypixel_key = hypixel_key[str(index)]
        return hypixel_key

with open('denylist.json') as f0:
    denylist = json.load(f0)

def update_denylist(update_data=None):
    global denylist
    with open('denylist.json') as u_f0:
        denylist = json.load(u_f0)

        if update_data != None:
            denylist['users'].append(str(update_data))

    return denylist

def scratch_denylist(remove_data):
        s_f0 = json.load(open("denylist.json"))

        print(s_f0['users'])
            
        for i in range(len(s_f0['users'])):
            if s_f0['users'][i] == remove_data:
                s_f0['users'].pop(i)
                break

        print(s_f0)

        open('denylist.json','w').write(json.dumps(s_f0))

from cogs.api import API

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def write_json(self, data, filename): 
        with open(filename,'w') as f: 
            json.dump(data, f, indent=1)
    
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


    @commands.command(name='update_keys', hidden=True, aliases=['uk'])
    @commands.is_owner()
    async def update_keys(self, ctx, key_id, key):
        global secrets


        secrets["Hypixel API Keys"][str(key_id)] = key

        json.dump(secrets, open('secrets.json', 'w'))

        if int(key_id) <= Key.key_index_len:

            await ctx.send('Updated Key')
        
        else:

            await ctx.send("Update Keys **`ERROR`** | \nInvalid Index of Key")


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

    @commands.command(name='add_denylist', hidden=True, aliases=['deny'])
    @commands.has_permissions(administrator=True)
    async def add_denylist(self, ctx, user):

        update_denylist(user)

        global denylist

        self.write_json(denylist, 'denylist.json')

        await ctx.send(f"Added user {user} to the deny list")


    @commands.command(name='remove_denylist', hidden=True, aliases=['undeny'])
    @commands.has_permissions(administrator=True)
    async def remove_denylist(self, ctx, user):

        update_denylist(user)

        global denylist

        try:
            scratch_denylist(user)
            await ctx.send(f'Removed {user}')
        except:
            await ctx.send(f"User {user} not found")

    @commands.command(name='list_denylist', hidden=True, aliases=['listdeny', 'denylist', 'ld'])
    @commands.has_permissions(administrator=True)
    async def list_denylist(self, ctx):

        update_denylist()
        global denylist

        msg = "```"

        for i in range(len(denylist['users'])):
            msg += denylist['users'][i]
            msg += "\n"

        msg += "```"
        
        await ctx.send(msg)



def setup(bot):
    bot.add_cog(Admin(bot))