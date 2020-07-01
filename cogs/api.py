from discord.ext import commands

import random
import requests
import json

from cogs.admin import Key

i = 0

class API(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def get_hypixel(self, uuid, hypixel_key=None, data='player'):

		global i
		i += 1
		i %= Key.key_index_len
		hypixel_key = Key.get_key(self, i)
		response =  None

		response = requests.get(f'https://api.hypixel.net/{data}?key={hypixel_key}&uuid={uuid}')
		response = json.loads(response.text)
		return response

	def get_key_info(self, key):
		response = requests.get(f"https://api.hypixel.net/key?key={key}")
		response = json.loads(response.text)

		key_info = None
		
		if response['success'] == True:
			data = response['record']
			key_info = [data['key'], data['owner'], data['totalQueries'], data['queriesInPastMin'], data['limit']]
		else:
			key_info = [False, "Invalid API Key!", key]

		return key_info

	def get_namemc(self, user):
		return f"namemc.com/profile/{user}"

	def get_ign(self, uuid):
		response = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")
		response = json.loads(response.text)
		try:
			ign = response[-1]['name']
		except:
			ign = '?'
		return ign

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

