from apscheduler.schedulers.blocking import BlockingScheduler
import json
import requests
from datetime import datetime


with open('secrets.json') as f0:
    secrets = json.load(f0)

hypixel_key = secrets['Hypixel API Keys']['0']

users = ['Satiated', 'Irron', 'hiiki', 'LividDucky', 'vegie']

class API:

    global hypixel_key

    def get_uuid(self, ign):
        response = ''
        uuid = None
        
        try:
            response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
            uuid = response['id']
            ign = response['name']
        except:
            raise ValueError('Invalid username')
        return [uuid, ign]

    def get_hypixel(self, uuid, data='player'):

        global hypixel_key

        response = requests.get(f'https://api.hypixel.net/{data}?key={hypixel_key}&uuid={uuid}')
        response = json.loads(response.text)

        return response



class Calcs:

    global hypixel_key

    def get_bw(self, ign: str) -> list:

        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)

        bedwars_stats = hypixel_data['player']['stats']['Bedwars']

        stars = ''
        try:
            stars = hypixel_data['player']['achievements']['bedwars_level']
        except:
            pass

        fkdr = ''
        final_kills = ''
        final_deaths = ''
        try:
            final_kills = int(bedwars_stats['final_kills_bedwars'])
            final_deaths = int(bedwars_stats['final_deaths_bedwars'])
            fkdr = round(final_kills / final_deaths, 2)
        except:
            pass
        
        winrate = ''
        try:
            wins = int(bedwars_stats['wins_bedwars'])
            losses = int(bedwars_stats['losses_bedwars'])
            winrate = wins / (wins + losses) * 100
            winrate = f'{winrate:.2f}%'
        except:
            pass

        winstreak = ''
        try:
            winstreak = bedwars_stats['winstreak']
        except:
            pass

        games = ''
        try:
            games = bedwars_stats['games_played_bedwars_1']
        except:
            pass

        beds = ''
        try:
            beds = bedwars_stats['beds_broken_bedwars']
        except:
            pass
        
        kills = ''
        try:
            kills = bedwars_stats['kills_bedwars']
        except:
            pass

        return [stars, fkdr, final_kills, final_deaths, kills, beds, games, winrate, winstreak]


def record_data():

    global users

    write_data = ''
    write_list = []

    #ign, stars, fkdr, final_kills, final_deaths, kills, beds, games, winrate, winstreak, time

    for i in range(len(users)):
        write_list.append(Calcs.get_bw(None, users[i]))

        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        write_data += (f"{users[i]}, " + str(write_list)[2:-2] + f", {current_time}\n")

        

        write_list = []
    
    with open("bedwars_data.csv", "a") as f:
        f.write(write_data.replace("'",''))

    write_list = ''

    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    print("Recorded Data at", current_time)

scheduler = BlockingScheduler()
scheduler.add_job(record_data, 'interval', hours=1)
scheduler.start()