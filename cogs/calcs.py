from decimal import HAVE_THREADS
from typing import List
import discord
from discord.ext import commands
import requests
from statistics import mean
import json
import math

from cogs.api import API
from cogs.admin import tiers

class Calcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_sw(self, ign: str) -> list:
        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)

        skywars_stats = hypixel_data['player']['stats']['SkyWars']

        stars = ''
        kdr_raw = ''
        kills = ''
        games = ''
        wins = ''
        winrate = ''
        kdr = ''
        heads = ''
        shards = ''
        opals = ''

        data = [stars, kdr_raw, kills, games, wins, winrate, heads, shards, opals]

        try:
            stars = round(Calcs.get_skywars_star(self, skywars_stats["skywars_experience"]), 2)
        except:
            stars = '?'

        try:
            kills = int(skywars_stats['kills'])
            deaths = int(skywars_stats['deaths'])
            kdr += str(round(kills / deaths, 2))
            kdr += f' ({kills}/{deaths})'
            kdr_raw = round(kills / deaths, 2)
        except:
            kdr = '?'
            kills = '?'
            kdr_raw = '?'
        
        try:
            wins = int(skywars_stats['wins'])
            losses = int(skywars_stats['losses'])
            winrate = wins / (wins + losses) * 100
            winrate = f'{winrate:.2f}%'
        except:
            winrate = '?'

        try:
            games = skywars_stats['games_played_skywars']
        except:
            games = '?'

        try:
            wins = skywars_stats['wins']
        except:
            wins = '?'
        
        try:
            kills = skywars_stats['kills']
        except:
            kills = '?'
    
        try:
            heads = skywars_stats['heads']
        except:
            heads = '?'
        
        try:
            shards = skywars_stats['shard']
        except:
            shards = '?'

        opals = ''
        try:
            opals = skywars_stats['opals']
        except:
            opals = '?'

        return data

    def get_bw(self, ign: str) -> list:
        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)

        stars = ''
        fkdr_raw = ''
        fkdr = ''
        final_kills = ''
        final_deaths = ''
        kills = ''
        deaths = ''
        bblr = ''
        beds_broken = ''
        beds_lost = ''
        winrate = ''
        wins = ''
        losses = ''
        games_played = ''
        winstreak = ''

        data = [stars, fkdr_raw, fkdr, final_kills, final_deaths, kills, deaths, bblr, beds_broken, beds_lost, winrate, wins, losses, games_played, winstreak]

        bedwars_stats = hypixel_data['player']['stats']['Bedwars']

        stars = hypixel_data['player']['achievements']['bedwars_level']
            #stars = f'[{stars}✫]'

        fkdr = str(round(final_kills / final_deaths, 2))
        fkdr += f' ({final_kills}/{final_deaths})'
        fkdr_raw = round(final_kills / final_deaths, 2)

        final_kills = int(bedwars_stats['final_kills_bedwars'])
        final_deaths = int(bedwars_stats['final_deaths_bedwars'])

        kills = bedwars_stats['kills_bedwars']
        deaths = bedwars_stats['deaths_bedwars']

        beds_broken = int(bedwars_stats['beds_broken_bedwars'])
        beds_lost = int(bedwars_stats['beds_lost_bedwars'])
        bblr = wins / (wins + losses) * 100
        bblr = f'{bblr:.2f}%'
        
        wins = int(bedwars_stats['wins_bedwars'])
        losses = int(bedwars_stats['losses_bedwars'])

        winrate = wins / (wins + losses) * 100
        winrate = f'{winrate:.2f}%'

        winstreak = bedwars_stats['winstreak']

        games_played = bedwars_stats['games_played_bedwars_1']

        return data

    def get_hypixel_network_level(self, exp: int) -> int:
        return (math.sqrt((2 * exp) + 30625) / 50) - 2.5

    def get_skywars_star(self, exp: int) -> int:
        xps = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
        if exp >= 15000:
            return (exp - 15000) / 10000. + 12
        else:
            for i in range(len(xps)):
                if exp < xps[i]:
                    return 0 + i + float(exp - xps[i-1]) / (xps[i] - xps[i-1])

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
    
    def is_online(self, uuid: str) -> bool:
        hypixel_data = API.get_hypixel(self, uuid)

        online = False

        try:
            if int(hypixel_data['player']["lastLogin"]) > int(hypixel_data['player']["lastLogout"]):
                online = True
        except:
            pass

        return online

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
            self.t_star = json.loads(tiers['star'])
            self.t_fkdr = json.loads(tiers['fkdr'])
            self.t_finals = json.loads(tiers['finals'])
            self.t_kills = json.loads(tiers['kills'])
            self.t_beds = json.loads(tiers['beds'])
            self.t_games = json.loads(tiers['games'])
            self.tiers_set = [
                self.t_star,
                self.t_fkdr,
                self.t_finals,
                self.t_kills,
                self.t_beds,
                self.t_games
            ]

        def get_closest(self, ign: str) -> List[int]:

            c_star = 0
            c_fkdr = 0
            c_finals = 0
            c_kills = 0
            c_beds = 0
            c_games = 0

            stats = Calcs.get_bw(self, ign)

            # c = closest

            stats_set = [
                c_star,
                c_fkdr,
                c_finals,
                c_kills,
                c_beds,
                c_games
                ]

            for i in range(len(stats_set)):
                stats_set[i] = min(self.tiers_set[i], key=(lambda list_value : abs(list_value - stats[i])))
                if stats[i] < stats_set[i]:
                    stats_set[i] = stats_set[i] = self.tiers_set[i].index(stats_set[i])-1
                elif stats[i] >= stats_set[i]:
                    stats_set[i] = self.tiers_set[i].index(stats_set[i])

            return [stats_set, round(mean(stats_set),0)]

        def get_difference(self, ign: str) -> list:
            stats = Calcs.get_bw(self, ign)

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

            closest = Calcs.Get_Tier.get_closest(self, ign)

            closest_rank = int(closest[1])
            closest_relatives = closest[0]

            relatives_set = [
                dr_star,
                dr_fkdr,
                dr_finals,
                dr_kills,
                dr_beds, 
                dr_games
            ]

            absolutes_set = [
                d_star,
                d_fkdr,
                d_finals,
                d_kills,
                d_beds, 
                d_games
            ]

            stats_set = []

            for i in range(len(relatives_set)):
                relatives_set[i] = round(stats[i]/self.tiers_set[i][closest_relatives[i]],2)

            for i in range(len(absolutes_set)):
                absolutes_set[i] = round(stats[i]/self.tiers_set[i][closest_rank],2)

            for i in range(len(relatives_set)):
                stats_set.append(relatives_set[i])

            for i in range(len(absolutes_set)):
                stats_set.append(absolutes_set[i])

            return [stats_set, round(mean(relatives_set),2), round(mean(absolutes_set),2)]

        def get_next_difference(self, ign: str):

            d_star = 0
            d_fkdr = 0
            d_finals = 0
            d_kills = 0
            d_beds = 0
            d_games = 0

            stats = Calcs.get_bw(self, ign)

            closest_relatives = Calcs.Get_Tier.get_closest(self, ign)[0]

            stats_set = [
                d_star,
                d_fkdr,
                d_finals,
                d_kills,
                d_beds, 
                d_games
            ]

            for i in range(len(stats_set)):
                stats_set[i] = round(self.tiers_set[i][closest_relatives[i]]-stats[i],2)
                if stats_set[i] < 0:
                    try:
                        stats_set[i] = round(self.tiers_set[i][closest_relatives[i]+1]-stats[i],2)
                    except:
                        pass
                        # There is not currently a tier above this stat value.

            return stats_set

        def to_romans(self, tier: int) -> str:
            romans = ["0","I","II","III","IV","V","VI","VII","VIII","IX","X"]
            return str(f"[Tier {romans[tier]}]")



def setup(bot):
    bot.add_cog(Calcs(bot))