import discord
from discord.ext import commands
from datetime import datetime, timezone
from discord.ui import View, Button
from discord.ext import commands, pages
import json
import wrapper

class Everyone(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_pages(self):
        with open('json/players.json') as fp:
            listObj = json.load(fp)

        pages = []
        for player in listObj['players']:
            embed=discord.Embed(title="Stalcraft Players", description=f"Username: {player['username']} \n Faction: {player['alliance']}")
            embed.add_field(name="Information:", value = f"""
            Player Kills: {next((x['value'] for x in player['stats'] if x['id'] == 'kil'),0):,}
            Headshots: {next((x['value'] for x in player['stats'] if x['id'] == 'sho-hea'),0):,}
            Deaths from Anomalies: {next((x['value'] for x in player['stats'] if x['id'] == 'ano-dea'),0):,}
            Longest Killstreak: {next((x['value'] for x in player['stats'] if x['id'] == 'max-kil-ser'),0):,}
            Shots Fired: {next((x['value'] for x in player['stats'] if x['id'] == 'sho-fir'),0):,}
            Bolts thrown: {next((x['value'] for x in player['stats'] if x['id'] == 'scr-thr'),0):,}
            Quests completed: {next((x['value'] for x in player['stats'] if x['id'] == 'que-fin'),0):,}
            """)
            pages.append(embed)
        
        return pages

    @discord.slash_command(description="List all current clans")
    async def everyone(self, ctx: discord.ApplicationContext):
        paginator = pages.Paginator(pages=self.get_pages(), loop_pages=True)
        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot):
    bot.add_cog(Everyone(bot))