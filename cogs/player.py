import discord
from discord.ext import commands
import wrapper
import json

class Players(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    player_command_group = discord.SlashCommandGroup("player", "Player related commands")

    @player_command_group.command(description="Gets the stats of a player")
    async def display(self, ctx, 
        region: discord.Option(str, choices=[
            "SEA",
            "RU",
            "EU",
            "NA",
        ]), 
        player_name: discord.Option(str)):

        player = await wrapper.get_player_profile(region,player_name)

        if player['status'] == 404:
            embed=discord.Embed(title="Stalcraft Players", description="User not found is the name right (Case senisitive)")
            await ctx.respond(embed=embed)
            return

        embed=discord.Embed(title="Stalcraft Players", description=f"Name: {player['username']} \n Faction: {player['alliance']}")
        embed.add_field(name="Stats", value=f"""
        Player Kills: {next((x['value'] for x in player['stats'] if x['id'] == 'kil'),0):,}
        Headshots: {next((x['value'] for x in player['stats'] if x['id'] == 'sho-hea'),0):,}
        Deaths from Anomalies: {next((x['value'] for x in player['stats'] if x['id'] == 'ano-dea'),0):,}
        Longest Killstreak: {next((x['value'] for x in player['stats'] if x['id'] == 'max-kil-ser'),0):,}
        Shots Fired: {next((x['value'] for x in player['stats'] if x['id'] == 'sho-fir'),0):,}
        Bolts thrown: {next((x['value'] for x in player['stats'] if x['id'] == 'scr-thr'),0):,}
        Quests completed: {next((x['value'] for x in player['stats'] if x['id'] == 'que-fin'),0):,}
        """, inline=False)
        await ctx.respond(embed=embed)  

    @player_command_group.command(description="Compares 2 players")
    async def compare(self, ctx, 
        region: discord.Option(str, choices = [
            "SEA",
            "RU",
            "EU",
            "NA",
            ]),
        player_name: discord.Option(str),
        region2: discord.Option(str, choices = [
            "SEA",
            "RU",
            "EU",
            "NA",
            ]),
        player2_name: discord.Option(str)):
        
        player1 = await wrapper.get_player_profile(region,player_name)
        player2 = await wrapper.get_player_profile(region2,player2_name)

        if player1['status'] == 404:
            embed=discord.Embed(title="Stalcraft Players", description=f"{player_name} not found is the name right (Case senisitive)")
            await ctx.respond(embed=embed)
            return
    
        if player2['status'] == 404:
            embed=discord.Embed(title="Stalcraft Players", description=f"{player2_name} not found is the name right (Case senisitive)")
            await ctx.respond(embed=embed)
            return
    
        kills = [next((x['value'] for x in player1['stats'] if x['id'] == 'kil'),0), next((x['value'] for x in player2['stats'] if x['id'] == 'kil'),0)]
        headshots = [next((x['value'] for x in player1['stats'] if x['id'] == 'sho-hea'),0), next((x['value'] for x in player2['stats'] if x['id'] == 'sho-hea'),0)]
        deaths = [next((x['value'] for x in player1['stats'] if x['id'] == 'ano-dea'),0), next((x['value'] for x in player2['stats'] if x['id'] == 'ano-dea'),0)]
        killstreak = [next((x['value'] for x in player1['stats'] if x['id'] == 'max-kil-ser'),0), next((x['value'] for x in player2['stats'] if x['id'] == 'max-kil-ser'),0)]
        shots_fired = [next((x['value'] for x in player1['stats'] if x['id'] == 'sho-fir'),0), next((x['value'] for x in player2['stats'] if x['id'] == 'sho-fir'),0)]
        bols_thrown = [next((x['value'] for x in player1['stats'] if x['id'] == 'scr-thr'),0), next((x['value'] for x in player2['stats'] if x['id'] == 'scr-thr'),0)]
        quests = [next((x['value'] for x in player1['stats'] if x['id'] == 'que-fin'),0), next((x['value'] for x in player2['stats'] if x['id'] == 'que-fin'),0)]

        embed=discord.Embed(title="Stalcraft Compare Players", description=f"""
        Comparing:
        {player1['username']} vs {player2['username']}
        {player1['alliance']} vs {player2['alliance']}
        """)

        embed.add_field(name=player1['username'], value=f"""
        Player Kills: {kills[0]:,}
        Headshots: {headshots[0]:,}
        Deaths from Anomalies: {deaths[0]:,}
        Longest Killstreak: {killstreak[0]:,}
        Shots Fired: {shots_fired[0]:,}
        Bolts thrown: {bols_thrown[0]:,}
        Quests completed: {quests[0]:,}
        """, inline=True)

        embed.add_field(name=player2['username'], value=f"""
        Player Kills: {kills[1]:,}
        Headshots: {headshots[1]:,}
        Deaths from Anomalies: {deaths[1]:,}
        Longest Killstreak: {killstreak[1]:,}
        Shots Fired: {shots_fired[1]:,}
        Bolts thrown: {bols_thrown[1]:,}
        Quests completed: {quests[1]:,}
        """, inline=True)
        await ctx.respond(embed=embed)  


def setup(bot):
    bot.add_cog(Players(bot))
