from typing import List
import discord
from discord.ext import commands
import requests
from statistics import mean
import json

from cogs.api import API
from cogs.admin import hypixel_key, tiers

class Calcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_stats(self, ign: str) -> list:
        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)

        bedwars_stats = hypixel_data['player']['stats']['Bedwars']

        stars = ''
        try:
            stars = hypixel_data['player']['achievements']['bedwars_level']
            #stars = f'[{stars}✫]'
        except:
            stars = '?'

        fkdr = ''
        final_kills = ''
        fkdr_raw = ''
        try:
            final_kills = int(bedwars_stats['final_kills_bedwars'])
            final_deaths = int(bedwars_stats['final_deaths_bedwars'])
            fkdr += str(round(final_kills / final_deaths, 2))
            fkdr += f' ({final_kills}/{final_deaths})'
            fkdr_raw = round(final_kills / final_deaths, 2)
        except:
            fkdr = '?'
            final_kills = '?'
            fkdr_raw = '?'
        
        winrate = ''
        try:
            wins = int(bedwars_stats['wins_bedwars'])
            losses = int(bedwars_stats['losses_bedwars'])
            winrate = wins / (wins + losses) * 100
            winrate = f'{winrate:.2f}%'
        except:
            winrate += '?'

        # Winstreak
        winstreak = ''
        try:
            winstreak = bedwars_stats['winstreak']
        except:
            winstreak = '?'

        games = ''
        try:
            games = bedwars_stats['games_played_bedwars_1']
        except:
            games = '?'

        beds = ''
        try:
            beds = bedwars_stats['beds_broken_bedwars']
        except:
            beds = '?'
        
        kills = ''
        try:
            kills = bedwars_stats['kills_bedwars']
        except:
            kills = '?'

        return [stars, fkdr, kills, winrate, winstreak, games, beds, final_kills, fkdr_raw]

    def get_socials(self, ign: str):
        
        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)

        social_discord = ''

        try:
            social_data = hypixel_data['player']['socialMedia']
    
            if "DISCORD" in social_data:
                social_discord += social_data['DISCORD']
                social_discord = social_discord.replace('1;','')
            else:
                pass
            
            if "links" in social_data:
                if 'DISCORD' in social_data['links']:
                    social_discord += social_data['links']['DISCORD']
            else:
                pass

            if social_discord == '':
                social_discord = 'UNKNOWN'

            return social_discord
        except:
            return 'UNKNOWN'

    def get_nick(self, nick: str) -> str:
        if "✫]" in nick:
            return nick[nick.index("]")+2:]
        else:
            return nick

    class Rank:

        def get_rank(self, ign: str):

            uuid = API.get_uuid(self, ign)[0]

            hypixel_data = API.get_hypixel(self, uuid)

            if 'newPackageRank' in hypixel_data['player']:
                return hypixel_data["player"]["newPackageRank"]
            else:
                return 0
            

        def get_sub(self, ign: str) -> int:

            uuid = API.get_uuid(self, ign)[0]

            hypixel_data = API.get_hypixel(self, uuid)

            if "monthlyPackageRank" in hypixel_data['player']:
                if hypixel_data['player']['monthlyPackageRank'] != 'NONE':
                    return 1
                else:
                    return 0
            else:
                return 0
        
        def get_staff(self, ign: str):

            uuid = API.get_uuid(self, ign)[0]

            hypixel_data = API.get_hypixel(self, uuid)

            if 'rank' in hypixel_data['player']:
                return hypixel_data["player"]["rank"]
            else:
                return 0
            
        
        def rank(self, ign: str) -> str:
            rank = ''
            
            if Calcs.Rank.get_staff(self, ign) != 0:
                rank = str(Calcs.Rank.get_staff(self, ign))
            else:
                    if Calcs.Rank.get_sub(self, ign) == 1:
                        rank = 'MVP++'
                    else:
                        if Calcs.Rank.get_rank(self, ign) != 0:
                            rank = str(Calcs.Rank.get_rank(self, ign))
                            if '_PLUS' in rank:
                                rank = rank.replace('_PLUS', '+')
                            else:
                                pass
                        else:
                            rank = 'Member'

            return rank

    class Get_Tier:
        
        # conver to list type
        def __init__(self) -> None:
            self.r_star = json.loads(tiers['star'])
            self.r_fkdr = json.loads(tiers['fkdr'])
            self.r_finals = json.loads(tiers['finals'])
            self.r_kills = json.loads(tiers['kills'])
            self.r_beds = json.loads(tiers['beds'])
            self.r_games = json.loads(tiers['games'])

        def get_closest(self, ign: str) -> List[int]:
            stats = Calcs.get_stats(self, ign)

            # c = closest
            c_star = min(self.r_star, key=(lambda list_value : abs(list_value - stats[0])))
            c_fkdr = min(self.r_fkdr, key=(lambda list_value : abs(list_value - stats[8])))
            c_finals = min(self.r_finals, key=(lambda list_value : abs(list_value - stats[7])))
            c_kills = min(self.r_kills, key=(lambda list_value : abs(list_value - stats[2])))
            c_beds = min(self.r_beds, key=(lambda list_value : abs(list_value - stats[6])))
            c_games = min(self.r_games, key=(lambda list_value : abs(list_value - stats[5])))

            stats_set = [
                self.r_star.index(c_star),
                self.r_fkdr.index(c_fkdr),
                self.r_finals.index(c_finals),
                self.r_kills.index(c_kills),
                self.r_beds.index(c_beds),
                self.r_games.index(c_games)
                ]
            return [stats_set, round(mean(stats_set),0)]

        def get_difference(self, ign: str) -> list:
            stats = Calcs.get_stats(self, ign)
            dr_star = 0
            dr_fkdr = 0
            dr_finals = 0
            dr_kills = 0
            dr_beds = 0
            dr_games = 0
            d_star = 0
            d_fkdr = 0
            d_finals = 0
            d_kills = 0
            d_beds = 0
            d_games = 0

            # d = difference
            
            # relative tier - stat to each closest rank
            closest_relatives = Calcs.Get_Tier.get_closest(self, ign)[0]
            try:
                dr_star = round(stats[0]/self.r_star[closest_relatives[0]],2)
                dr_fkdr = round(stats[8]/self.r_fkdr[closest_relatives[1]],2)
                dr_finals = round(stats[7]/self.r_finals[closest_relatives[2]],2)
                dr_kills = round(stats[2]/self.r_kills[closest_relatives[3]],2)
                dr_beds = round(stats[6]/self.r_beds[closest_relatives[4]],2)
                dr_games = round(stats[5]/self.r_games[closest_relatives[5]],2)
            except:
                pass

            closest_rank = int(Calcs.Get_Tier.get_closest(self, ign)[1])

            d_star = round(stats[0]/self.r_star[closest_rank],2)
            d_fkdr = round(stats[8]/self.r_fkdr[closest_rank],2)
            d_finals = round(stats[7]/self.r_finals[closest_rank],2)
            d_kills = round(stats[2]/self.r_kills[closest_rank],2)
            d_beds = round(stats[6]/self.r_beds[closest_rank],2)
            d_games = round(stats[5]/self.r_games[closest_rank],2)

            stats_set = [
                dr_star,
                dr_fkdr,
                dr_finals,
                dr_kills,
                dr_beds, 
                dr_games,
                d_star,
                d_fkdr,
                d_finals,
                d_kills,
                d_beds, 
                d_games
            ]

            return [stats_set, round(mean(stats_set[:6]),2), round(mean(stats_set[6:]),2)]

        def to_romans(self, tier: str) -> str:
            romans = ["I","II","III","IV","V","VI","VII"]
            return str(f"[Tier {romans[tier-1]}]")



def setup(bot):
    bot.add_cog(Calcs(bot))