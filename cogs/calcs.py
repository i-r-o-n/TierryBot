import discord
from discord.ext import commands
import requests
from statistics import mean
from cogs.admin import hypixel_key

#tier levels dictionaries
star_ranks = (0,50,100,150,200,300,700,1000)
kills_ranks = (0,1500,3000,4500,6000,9000,21000,30000)
fkdr_ranks = (0,0.6,1,1.4,1.83,2.68,5.81,7.75)
finals_ranks = (0,363,1000,1810,2757,4989,17230,29034)
games_ranks = (0,500,1066,1684,2350,3810,11106,17907)
beds_ranks = (0,181,500,905,1378,2494,8651,14517)

class Calcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #general bedwars api retrieve
    def Retrieve(self, ign, stat):
        data = requests.get(f"https://api.hypixel.net/player?key={hypixel_key}&name={ign}").json()
        return data["player"]["stats"]["Bedwars"][stat] if stat in data["player"]["stats"]["Bedwars"] else 0

    # Star Calculations

    #determine prestige of player, each 100 stars (480,000 xp) is 1 prestige
    def GetPrestige(self, xp):
        if xp < 0:
            return 0
        elif 0 < xp < 480000:
            return 0
        elif 480000 < xp < 960000:
            return 1
        elif 960000 < xp < 1440000:
            return 2
        elif 1440000 < xp < 1920000:
            return 3
        elif 1920000 < xp < 2400000:
            return 4
        elif 2400000 < xp < 2880000:
            return 5
        elif 2880000 < xp < 3360000:
            return 6
        elif 3360000 < xp < 3840000:
            return 7
        elif 3840000 < xp < 4320000:
            return 8
        elif 4320000 < xp < 480000:
            return 9
        else:
            return 0

    #determine stars based on xp. extra calculations due to xp curve being non-linear at the beginning of each prestiege.
    def StarsfromXP(self, ign):
        stars_fxn = (Calcs.Retrieve(self, ign, "Experience") + ((Calcs.GetPrestige(self, Calcs.Retrieve(self, ign, "Experience")) + 1)*12000))/5000
        return stars_fxn

    #return the closest rank (index in the stat dictionary) for each of the player's stats
    def ClosestRank(self, ign):
        global star_ranks
        global kills_ranks
        global fkdr_ranks
        global finals_ranks
        global games_ranks
        global beds_ranks

        games_played = Calcs.Retrieve(self, ign, "games_played_bedwars_1")
        beds_broken = Calcs.Retrieve(self, ign, "beds_broken_bedwars")
        stars = Calcs.StarsfromXP(self, ign)
        fkdr = (Calcs.Retrieve(self, ign, "final_kills_bedwars"))/(Calcs.Retrieve(self, ign, "final_deaths_bedwars"))
        kills = Calcs.Retrieve(self, ign, "kills_bedwars")
        finals = Calcs.Retrieve(self, ign, "final_kills_bedwars")

        #gives closest tier for each stat
        closest_star = min(star_ranks, key=(lambda list_value : abs(list_value - stars)))
        closest_kills = min(kills_ranks, key=(lambda list_value : abs(list_value - kills)))
        closest_fkdr = min(fkdr_ranks, key=(lambda list_value : abs(list_value - fkdr)))
        closest_finals = min(finals_ranks, key=(lambda list_value : abs(list_value - finals)))
        closest_games = min(games_ranks, key=(lambda list_value : abs(list_value - games_played)))
        closest_beds = min(beds_ranks, key=(lambda list_value : abs(list_value - beds_broken)))

        stats_set = [star_ranks.index(closest_star),kills_ranks.index(closest_kills),fkdr_ranks.index(closest_fkdr),finals_ranks.index(closest_finals),games_ranks.index(closest_games),beds_ranks.index(closest_beds)]
        return [stats_set, round(mean(stats_set),0)]

    #return the difference between the player's stat and the tier stat of the closest tier for each stat
    def Difference(self, ign):
        global star_ranks
        global kills_ranks
        global fkdr_ranks
        global finals_ranks
        global games_ranks
        global beds_ranks

        ign_stars = Calcs.StarsfromXP(self, ign)

        kills_dif = (Calcs.Retrieve(self, ign, "kills_bedwars")) / kills_ranks[int(Calcs.ClosestRank(self, ign)[1])]

        fkdr_dif = (Calcs.Retrieve(self, ign, "final_kills_bedwars") / Calcs.Retrieve(self, ign, "final_deaths_bedwars")) / fkdr_ranks[int(Calcs.ClosestRank(self, ign)[1])]

        finals_dif = (Calcs.Retrieve(self, ign, "final_kills_bedwars")) / finals_ranks[int(Calcs.ClosestRank(self, ign)[1])]

        games_dif = (Calcs.Retrieve(self, ign, "games_played_bedwars_1")) / games_ranks[int(Calcs.ClosestRank(self, ign)[1])]

        beds_dif = Calcs.Retrieve(self, ign, "beds_broken_bedwars") / beds_ranks[int(Calcs.ClosestRank(self, ign)[1])]

        return [ign_stars, [kills_dif, fkdr_dif, finals_dif, games_dif, beds_dif]]

    # EDIT!
    #formatting the role text into roman characters for discord roles
    def GetRole(self, tier):
        romans = ["I","II","III","IV","V","VI","VII"]
        return str("Tier "+romans[tier-1])

    def RankDisplay(self, tier, stat):
        if isinstance(tier,list):
            return stat[(tier[0]-1):(tier[1]-1)]
        else:
            if tier == 0:
                return stat[:]
            elif 0 < round(tier,0) <= 7:
                return stat[round(tier,0)]
            else:
                return stat[:]

    @commands.command(name='ranks', aliases=['r'])
    async def ranks(self, ctx, tier=0):
        global star_ranks
        global kills_ranks
        global fkdr_ranks
        global finals_ranks
        global games_ranks
        global beds_ranks

        embed = discord.Embed(
            color=discord.Color.blue(),
            title="Bedwars Tiers",
            description="""Displaying Stat requirements for each tier\n
            Specify a tier or leave arguments blank for all tiers.\n
            NOTE: in the future -> Use range of tier values by list object \"[tier1,tier2]\""""
        )

        embed.set_author(name="TIERS")
        embed.add_field(name="Star ranks", value=Calcs.RankDisplay(self, tier, star_ranks), inline=False)
        embed.add_field(name="Kill ranks", value=Calcs.RankDisplay(self, tier, kills_ranks), inline=False)
        embed.add_field(name="FKDR ranks", value=Calcs.RankDisplay(self, tier, fkdr_ranks), inline=False)
        embed.add_field(name="Finals ranks", value=Calcs.RankDisplay(self, tier, finals_ranks), inline=False)
        embed.add_field(name="Games Played ranks", value=Calcs.RankDisplay(self, tier, games_ranks), inline=False)
        embed.add_field(name="Beds Broken ranks", value=Calcs.RankDisplay(self, tier, beds_ranks), inline=False)
        embed.set_footer(text="Bedwars Tier Bot || Built by @Iron#1337 et al.")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Calcs(bot))