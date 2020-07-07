import discord
from discord.ext import commands

import traceback
import logging

from cogs.admin import token

# NOTE: search for the text "EDIT!" to find proprietary code that can be changed

game_acitivity = '.help | Bedwars ✫ Ranking'

# create a log of discord events
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def get_prefix(bot, message):

    prefixes = ['.', '/']

    if not message.guild:
        return '?'
    
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.api',
                      'cogs.admin',
                      'cogs.party',
                      'cogs.general',
                      'cogs.calcs',
                      'cogs.tier',
                      'cogs.error']


bot = commands.Bot(command_prefix=get_prefix, description='Bedwars Tier Bot')

# Notice: the way this bot is coded appeals to readability rather than kindness to the hypixel api. Commands are slow due to multiple requests on the api.

if __name__ in '__main__':
  for extension in initial_extensions:
    try:
      bot.load_extension(extension)
    except Exception as e:
      traceback.print_exc()

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    global game_acitivity

    await bot.change_presence(activity=discord.Game(name=game_acitivity, type=1))
    print(f'Successfully logged in and booted.')


bot.run(token, bot=True, reconnect=True)