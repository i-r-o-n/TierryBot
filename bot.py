import discord
from discord.ext import commands
import sys, traceback

import discord
import logging

from cogs.admin import TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#with open('secrets.json') as f:
#    TOKEN = json.load(f)

#TOKEN = TOKEN['TOKEN']

def get_prefix(bot, message):

    prefixes = ['.', '/']

    if not message.guild:
        return '?'
    
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.general',
                      'cogs.admin',
                      'cogs.tests',
                      'cogs.tiers',
                      'cogs.errors',
                      'cogs.calcs',
                      'cogs.party']

bot = commands.Bot(command_prefix=get_prefix, description='Bedwars Tier Bot')

if __name__ in '__main__':
  for extension in initial_extensions:
    try:
      bot.load_extension(extension)
    except Exception as e:
      traceback.print_exc()

# NOTE: search for the text "EDIT!" to find proprietary code in need of changing.

### Generic Events

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name='Calculating Bedwars Tiers', type=1, url='https://www.twitch.tv/directory/game/Minecraft'))
    print(f'Successfully logged in and booted...!')


bot.run(TOKEN, bot=True, reconnect=True)