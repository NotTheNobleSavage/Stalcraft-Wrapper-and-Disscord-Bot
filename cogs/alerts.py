import discord
from discord.ext import commands
from datetime import datetime, timezone
import json
import wrapper
import asyncio

class Alerts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regions = ["RU","EU","NA","SEA","ALL"]
        self.emission_times = {region: None for region in self.regions}
        
    @discord.slash_command(description="Setup alerts.")
    #Setups the channel you want to alert in
    async def alert(self,ctx, 
        region: discord.Option(str, choices=[
            "SEA",
            "RU",
            "EU",
            "NA",
            "ALL"
        ]),
        option: discord.Option(str, choices=[
            "Add",
            "View",
            "Remove"
        ])
    ):

        #Opens the server config as listObj and closes it
        with open('json/server_config.json') as fp:
            listObj = json.load(fp)

        #Checks
        #Check for permission
        if not ctx.user.guild_permissions.administrator:
            embed=discord.Embed(title="Emission Checker", description="You have no power here")
            await ctx.respond(embed=embed)
            return
        
        if option == 'Add':
            #Checks to see if there is already an alert for this region
            if {"guild_id": ctx.guild_id,"alert_channel": ctx.channel_id,"region": region} in listObj['servers']:
                embed=discord.Embed(title="Emission Checker", description=f"You already have an emission alert for the {region} Region in this channel ")
                await ctx.respond(embed=embed) 
                return

            #Checks to see if they have all reagions setup for alerting
            if {"guild_id": ctx.guild_id,"alert_channel": ctx.channel_id,"region": 'ALL'} in listObj['servers']:
                embed=discord.Embed(title="Emission Checker", description=f"You already have an emission alert for all regions in this channel ")
                await ctx.respond(embed=embed) 
                return

            #Create and append the new alert to the listObj and rewrite the json/server_config file
            listObj['servers'].append({"guild_id": ctx.guild_id,"alert_channel": ctx.channel_id,"region": region})
            with open('json/server_config.json', 'w') as json_file:
                json.dump(listObj, json_file, indent=4,separators=(',',': '))

            #Send secusses message
            embed=discord.Embed(title="Emission Checker", description=f"The Alert for the {region} region has been added")

        if option == 'View':
            matching_servers = [server['region'] for server in listObj['servers'] if server['guild_id'] == ctx.guild_id and server['alert_channel'] == ctx.channel_id]
            #Checks
            #Check to see if the guild has any alerts
            if not matching_servers:
                embed=discord.Embed(title="Emission Checker", description="There not no alerts setup in this channel")
                await ctx.respond(embed=embed)
                return
            
            #Main code prints the guilds alert
            embed=discord.Embed(title="Emission Checker", description="Here are the current alerts for this channel")
            embed.add_field(name="Region:", value='\n'.join(e for e in matching_servers), inline=False)
        
        if option =='Remove':
            matching_servers = [server['region'] for server in listObj['servers'] if server['guild_id'] == ctx.guild_id]
            #Checks
            #Check for permission
            if not ctx.user.guild_permissions.administrator:
                embed=discord.Embed(title="Emission Checker", description="You have no power here")
                await ctx.respond(embed=embed)
                return

            if not {"guild_id": ctx.guild_id,"alert_channel": ctx.channel_id,"region": region} in listObj['servers']:
                embed=discord.Embed(title="Emission Checker", description="There not no alerts setup in this channel")
                await ctx.respond(embed=embed)   
                return

            matching_servers = [server for server in listObj['servers'] if server == {"guild_id": ctx.guild_id,"alert_channel": ctx.channel_id,"region": region}]
            for server in matching_servers:
                listObj['servers'].remove(server)
            with open('json/server_config.json', 'w') as json_file:
                json.dump(listObj, json_file, indent=4,separators=(',',': '))

            embed=discord.Embed(title="Emission Checker", description=f"The Alert for {region} has been removed")
        
        await ctx.respond(embed=embed) 

def setup(bot):
    bot.add_cog(Alerts(bot))