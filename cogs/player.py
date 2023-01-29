import discord
from discord.ext import commands
import wrapper
import json

class Players(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Gets the stats of a player")
    async def get_player(self, ctx, region: discord.Option(str), player_name: discord.Option(str)):
        player = await wrapper.get_player_profile(region,player_name)

        if player['status'] == 404:
            embed=discord.Embed(title="Stalcraft Players", description="User not found is the name right (Case senisitive)")
            await ctx.respond(embed=embed)
            return
    
        if player['status'] == 400:
            embed=discord.Embed(title="Stalcraft Players", description="Please Enter a Valid Region: RU, EU, NA, SEA")
            await ctx.respond(embed=embed)
            return

        with open('json/stats.json', encoding='utf8') as fp:
            stats_translate = json.load(fp)

        for stats in player['stats']:
            for ids in stats_translate:
                if stats['id'] == ids['id']:
                    stats.update({'name':ids['name']['lines']['en']})
        
        embed=discord.Embed(title="Stalcraft Players", description=f"Name: {player['username']} \n Faction: {player['alliance']}")
        embed.add_field(name="Stats", value=f"""
        Player Kills: {[x['value'] for x in player['stats'] if x['id'] == 'kil'][0]}
        Headshots: {[x['value'] for x in player['stats'] if x['id'] == 'sho-hea'][0]}
        Deaths from Anomalies: {[x['value'] for x in player['stats'] if x['id'] == 'ano-dea'][0]}
        Longest Killstreak: {[x['value'] for x in player['stats'] if x['id'] == 'max-kil-ser'][0]}
        Shots Fired: {[x['value'] for x in player['stats'] if x['id'] == 'sho-fir'][0]}
        Bolts thrown: {[x['value'] for x in player['stats'] if x['id'] == 'scr-thr'][0]}
        Quests completed: {[x['value'] for x in player['stats'] if x['id'] == 'que-fin'][0]}
        """, inline=False)
        await ctx.respond(embed=embed)  

def setup(bot):
    bot.add_cog(Players(bot))
