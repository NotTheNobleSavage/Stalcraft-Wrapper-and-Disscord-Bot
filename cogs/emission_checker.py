import discord
from discord.ext import commands
from datetime import datetime, timezone
import wrapper
import asyncio
import json
import os

class Emission_checker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regions = ["RU","EU","NA","SEA","ALL"]
        self.emission_times = {region: None for region in self.regions}

    async def check_for_emissions(self):
        with open(os.path.normpath('json/server_config.json'), encoding='utf8') as config_file:
            server_options = json.load(config_file)

        for region in self.regions[:-1]:
            emission = await wrapper.get_emission(region)
            if self.emission_times[region] != emission['previousStart'] and 'currentStart' in emission:
                self.emission_times[region] = emission['previousStart']
                emission_datetime = datetime.strptime(emission['currentStart'], '%Y-%m-%dT%H:%M:%SZ')
                emission_timestamp = emission_datetime.replace(tzinfo=timezone.utc).timestamp()
                for server in server_options['servers']:
                    if server['region'] == region or server['region'] == 'ALL':
                        channel = self.bot.get_channel(int(server['alert_channel']))
                        if channel != None:
                            embed = discord.Embed(title="Emission Checker", description=f"A Emission is occurring in: {region}")
                            embed.add_field(name="Start of Emission", value=f"<t:{int(emission_timestamp)}>", inline=True)
                            embed.set_footer(text="Powered by NobleNet")
                            try:
                                await channel.send(embed=embed)
                            except discord.Forbidden:
                                print(f"cant send msg in {channel}")

    @commands.Cog.listener()
    async def on_ready(self): # this is called when a member joins the server     
        while True:
            await self.check_for_emissions()
            await asyncio.sleep(10)

def setup(bot):
    bot.add_cog(Emission_checker(bot))