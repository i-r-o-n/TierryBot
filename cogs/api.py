from discord.ext import commands

import random
import requests
import json

from cogs.admin import Key

i = 0

class API(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def get_hypixel(self, uuid, hypixel_key=None, data='player', id_tag='uuid'):

		global i
		i += 1
		i %= Key.key_index_len
		hypixel_key = Key.get_key(self, i)
		response =  None

		response = requests.get(f'https://api.hypixel.net/{data}?key={hypixel_key}&{id_tag}={uuid}')
		response = json.loads(response.text)
		print(i)
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
		return [uuid, ign]

	def get_guild(self, ign):
		uuid = API.get_uuid(self, ign)[0]

		g_uuid = API.get_hypixel(self, uuid, data='findGuild', id_tag='byUuid')

		guild_name = '?'

		if g_uuid['success'] == True:
			g_uuid = g_uuid['guild']

		guild = API.get_hypixel(self, g_uuid, data='guild', id_tag='id')

		if guild['success'] == True:
			guild_name = guild['guild']['name']

		return guild_name

def setup(bot):
    bot.add_cog(API(bot))

