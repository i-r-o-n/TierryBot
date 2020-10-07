from decimal import HAVE_THREADS
from os import stat
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

        data = [stars, kdr_raw, kills, games, wins, winrate, heads, shards, opals]

        return data

    def get_bw(self, ign: str, mode=0) -> list:
        uuid = API.get_uuid(self, ign)[0]

        hypixel_data = API.get_hypixel(self, uuid)

        stars = 0
        fkdr_raw = 0
        fkdr = 0
        final_kills = 0
        final_deaths = 0
        kills = 0
        deaths = 0
        bblr = 0
        beds_broken = 0
        beds_lost = 0
        wlr = 0
        wins = 0
        losses = 0
        games_played = 0
        winstreak = 0
        resources = [0,0]

        bw_stats = hypixel_data['player']['stats']['Bedwars']

        stars = hypixel_data['player']['achievements']['bedwars_level']
            #stars = f'[{stars}✫]'

        index_names = ['','eight_one_', 'eight_two_', 'four_three_', 'four_four_']
        chosen_index = ''

        for i in range(0,5):
            if mode == i:
                chosen_index = index_names[i]

        print(chosen_index)

        final_kills = int(bw_stats[chosen_index + 'final_kills_bedwars'])
        final_deaths = int(bw_stats[chosen_index + 'final_deaths_bedwars'])

        fkdr = str(round(final_kills / final_deaths, 2))
        fkdr += f' ({final_kills}/{final_deaths})'
        fkdr_raw = round(final_kills / final_deaths, 2)

        kills = bw_stats[chosen_index + 'kills_bedwars']
        deaths = bw_stats[chosen_index + 'deaths_bedwars']

        kdr = round(kills / deaths, 2)

        try:
            beds_broken = int(bw_stats[chosen_index + 'beds_broken_bedwars'])
        except:
            pass
        try:
            beds_lost = int(bw_stats[chosen_index + 'beds_lost_bedwars'])
        except:
            pass
        try:
            bblr = round(beds_broken / beds_lost, 2)
        except:
            bblr = beds_broken
        
        wins = int(bw_stats[chosen_index + 'wins_bedwars'])
        losses = int(bw_stats[chosen_index + 'losses_bedwars'])

        wlr = wins / (wins + losses) * 100
        wlr = f'{wlr:.2f}%'

        winstreak = bw_stats[chosen_index + 'winstreak']

        games_played = wins + losses

        resources = [bw_stats[chosen_index + "iron_resources_collected_bedwars"], bw_stats[chosen_index + "gold_resources_collected_bedwars"]]
        
        return [stars, fkdr_raw, fkdr, final_kills, final_deaths, kdr, kills, deaths, bblr, beds_broken, beds_lost, wlr, wins, losses, games_played, winstreak, resources]

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
        
        # t = tier
        def __init__(self) -> None:
            self.t_stars = json.loads(tiers['stars'])
            self.t_fkdr = json.loads(tiers['fkdr'])
            self.t_final_kills = json.loads(tiers['final_kills'])
            self.t_kills = json.loads(tiers['kills'])
            self.t_bblr = json.loads(tiers['bblr'])
            self.t_beds_broken = json.loads(tiers['beds_broken'])
            self.t_wlr = json.loads(tiers['winrate'])
            self.t_wins = json.loads(tiers['wins'])
            self.t_games_played = json.loads(tiers['games_played'])
            self.tiers_set = [
                self.t_stars,
                self.t_fkdr,
                self.t_final_kills,
                self.t_kills,
                self.t_bblr,
                self.t_beds_broken,
                self.t_wlr,
                self.t_wins,
                self.t_games_played
            ]
            return self.tiers_set

        def get_closest(self, ign: str) -> List[int]:

            # c = closest

            c_stars = 0
            c_fkdr = 0
            c_final_kills = 0
            c_kills = 0
            c_bblr = 0
            c_beds_broken = 0
            c_wlr = 0
            c_wins = 0
            c_games_played = 0

            stats = Calcs.get_bw(self, ign)
            #[stars, fkdr_raw, fkdr, final_kills, final_deaths, kdr, kills, deaths, bblr, beds_broken, beds_lost, wlr, wins, losses, games_played, winstreak, resources]
            #[stars, fkdr_raw, final_kills, kills, bblr, beds_broken, wlr, wins, games_played]
            abbv_list = [0,1,3,6,8,9,11,12,14]

            stats_set = [
                c_stars,
                c_fkdr,
                c_final_kills,
                c_kills,
                c_bblr,
                c_beds_broken,
                c_wlr,
                c_wins,
                c_games_played,
                ]


            for i in range(len(stats_set)):
                stats_value = 0
                if i == 6:
                    stats_value = float(stats[abbv_list[i]][0:-1])
                else:
                    stats_value = float(stats[abbv_list[i]])
                
                stats_set[i] = min(self.tiers_set[i], key=(lambda list_value : abs(list_value - stats_value)))
                if stats_value < stats_set[i]:
                    stats_set[i] = stats_set[i] = self.tiers_set[i].index(stats_set[i])-1
                elif stats_value >= stats_set[i]:
                    stats_set[i] = self.tiers_set[i].index(stats_set[i])

            return [stats_set, round(mean(stats_set),0)]

        def get_difference(self, ign: str) -> list:

            stats = Calcs.get_bw(self, ign)

            dr_stars = 0
            dr_fkdr = 0
            dr_final_kills = 0
            dr_kills = 0
            dr_bblr = 0
            dr_beds_broken = 0
            dr_wlr = 0
            dr_wins = 0
            dr_games_played = 0
            
            d_stars = 0
            d_fkdr = 0
            d_final_kills = 0
            d_kills = 0
            d_bblr = 0
            d_beds_broken = 0
            d_wlr = 0
            d_wins = 0
            d_games_played = 0

            # d = difference
            
            # relative tier - stat to each closest rank

            closest = Calcs.Get_Tier.get_closest(self, ign)

            closest_rank = int(closest[1])
            closest_relatives = closest[0]

            relatives_set = [
                dr_stars,
                dr_fkdr,
                dr_final_kills,
                dr_kills,
                dr_bblr,
                dr_beds_broken,
                dr_wlr,
                dr_wins,
                dr_games_played,
            ]

            absolutes_set = [
                d_stars,
                d_fkdr,
                d_final_kills,
                d_kills,
                d_bblr,
                d_beds_broken,
                d_wlr,
                d_wins,
                d_games_played,
            ]

            abbv_list = [0,1,3,6,8,9,11,12,14]

            stats_set = []

            stats_value = []

            for i in range(len(relatives_set)):
                
                if i == 6:
                    stats_value.append(float(stats[abbv_list[i]][0:-1]))
                else:
                    stats_value.append(float(stats[abbv_list[i]]))

            for i in range(len(relatives_set)):
                relatives_set[i] = round(stats_value[i]/self.tiers_set[i][closest_relatives[i]],2)

            for i in range(len(absolutes_set)):
                absolutes_set[i] = round(stats_value[i]/self.tiers_set[i][closest_rank],2)

            return [relatives_set, absolutes_set, round(mean(relatives_set),2), round(mean(absolutes_set),2)]

        def get_next_difference(self, ign: str):

            d_stars = 0
            d_fkdr = 0
            d_final_kills = 0
            d_kills = 0
            d_bblr = 0
            d_beds_broken = 0
            d_wlr = 0
            d_wins = 0
            d_games_played = 0

            stats = Calcs.get_bw(self, ign)

            abbv_list = [0,1,3,6,8,9,11,12,14]

            stats_value = []

            closest_relatives = Calcs.Get_Tier.get_closest(self, ign)[0]

            stats_set = [
                d_stars,
                d_fkdr,
                d_final_kills,
                d_kills,
                d_bblr,
                d_beds_broken,
                d_wlr,
                d_wins,
                d_games_played,
            ]

            for i in range(len(stats_set)):
                
                if i == 6:
                    stats_value.append(float(stats[abbv_list[i]][0:-1]))
                else:
                    stats_value.append(float(stats[abbv_list[i]]))

            for i in range(len(stats_set)):
                stats_set[i] = round(self.tiers_set[i][closest_relatives[i]]-stats_value[i],2)
                if stats_set[i] < 0:
                    try:
                        stats_set[i] = round(self.tiers_set[i][closest_relatives[i]+1]-stats_value[i],2)
                    except:
                        pass
                        # There is not currently a tier above this stat value.

            return stats_set

        def to_romans(self, tier: int) -> str:
            romans = ["I","II","III","IV","V","VI","VII","VIII","IX","X"]
            return str(f"[Tier {romans[tier-1]}]")



def setup(bot):
    bot.add_cog(Calcs(bot))