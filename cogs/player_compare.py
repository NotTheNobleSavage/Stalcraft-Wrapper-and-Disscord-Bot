import discord
from discord.ext import commands
import wrapper
import json

class Players_Compare(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Compares 2 players")
    async def players_compare(self, ctx, region: discord.Option(str), player_name: discord.Option(str), region2: discord.Option(str), player2_name: discord.Option(str)):
        player1 = await wrapper.get_player_profile(region,player_name)
        player2 = await wrapper.get_player_profile(region2,player2_name)

        if player1['status'] == 404:
            embed=discord.Embed(title="Stalcraft Players", description="User not found is the name right (Case senisitive)")
            await ctx.respond(embed=embed)
            return
    
        if player1['status'] == 400:
            embed=discord.Embed(title="Stalcraft Players", description="Please Enter a Valid Region: RU, EU, NA, SEA")
            await ctx.respond(embed=embed)
            return

        if player2['status'] == 404:
            embed=discord.Embed(title="Stalcraft Players", description="User not found is the name right (Case senisitive)")
            await ctx.respond(embed=embed)
            return
    
        if player2['status'] == 400:
            embed=discord.Embed(title="Stalcraft Players", description="Please Enter a Valid Region: RU, EU, NA, SEA")
            await ctx.respond(embed=embed)
            return

        with open('json/stats.json', encoding='utf8') as fp:
            stats_translate = json.load(fp)

        for stats in player1['stats']:
            for ids in stats_translate:
                if stats['id'] == ids['id']:
                    stats.update({'name':ids['name']['lines']['en']})

        for stats in player2['stats']:
            for ids in stats_translate:
                if stats['id'] == ids['id']:
                    stats.update({'name':ids['name']['lines']['en']})
        
        kills = [[x['value'] for x in player1['stats'] if x['id'] == 'kil'][0], [x['value'] for x in player2['stats'] if x['id'] == 'kil'][0]]
        headshots = [[x['value'] for x in player1['stats'] if x['id'] == 'sho-hea'][0], [x['value'] for x in player2['stats'] if x['id'] == 'sho-hea'][0]]
        deaths = [[x['value'] for x in player1['stats'] if x['id'] == 'ano-dea'][0], [x['value'] for x in player2['stats'] if x['id'] == 'ano-dea'][0]]
        killstreak = [[x['value'] for x in player1['stats'] if x['id'] == 'max-kil-ser'][0], [x['value'] for x in player2['stats'] if x['id'] == 'max-kil-ser'][0]]
        shots_fired = [[x['value'] for x in player1['stats'] if x['id'] == 'sho-fir'][0], [x['value'] for x in player2['stats'] if x['id'] == 'sho-fir'][0]]
        bols_thrown = [[x['value'] for x in player1['stats'] if x['id'] == 'scr-thr'][0], [x['value'] for x in player2['stats'] if x['id'] == 'scr-thr'][0]]
        quests = [[x['value'] for x in player1['stats'] if x['id'] == 'que-fin'][0], [x['value'] for x in player2['stats'] if x['id'] == 'que-fin'][0]]

        embed=discord.Embed(title="Stalcraft Compare Players", description=f"""
        Comparing:
        {player1['username']} vs {player2['username']}
        {player1['alliance']} vs {player2['alliance']}
        """)

        embed.add_field(name=player1['username'], value=f"""
        Player Kills: {kills[0]}
        Headshots: {headshots[0]}
        Deaths from Anomalies: {deaths[0]}
        Longest Killstreak: {killstreak[0]}
        Shots Fired: {shots_fired[0]}
        Bolts thrown: {bols_thrown[0]}
        Quests completed: {quests[0]}
        """, inline=True)

        embed.add_field(name=player2['username'], value=f"""
        Player Kills: {kills[1]}
        Headshots: {headshots[1]}
        Deaths from Anomalies: {deaths[1]}
        Longest Killstreak: {killstreak[1]}
        Shots Fired: {shots_fired[1]}
        Bolts thrown: {bols_thrown[1]}
        Quests completed: {quests[1]}
        """, inline=True)
        await ctx.respond(embed=embed)  

def setup(bot):
    bot.add_cog(Players_Compare(bot))
