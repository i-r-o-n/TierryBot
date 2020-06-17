from discord.ext import commands


import requests
import json

from cogs.admin import hypixel_key

class API(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def get_hypixel(self, uuid, hypixel_key=hypixel_key, data='player'):
		response =  None
		try:
			response = requests.get(f'https://api.hypixel.net/{data}?key={hypixel_key}&uuid={uuid}')
			response = json.loads(response.text)
		except:
			pass
		return response


	def get_uuid(self, ign):
		response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')
		response = json.loads(response.text)
		uuid = None
		
		try:
			uuid = response['id']
			ign = response['name']
		except:
			raise ValueError('Invalid username')
		return (uuid, ign)

def setup(bot):
    bot.add_cog(API(bot))

