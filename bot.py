#WE USE PYCORD HERE NOT DISCORD.PY
import discord

#Auth and Wrapper
import auth
import wrapper

#Python modules
from datetime import datetime
from datetime import timezone
import asyncio
import os
import json

bot = discord.Bot()


#Code to check if the emission is happaning
regions = ["RU","EU","NA","SEA","ALL"]
emission_times = {region: None for region in regions}

with open(os.path.normpath('server_config.json'), encoding='utf8') as config_file:
    server_options = json.load(config_file)

async def check_for_emissions():
    with open(os.path.normpath('server_config.json'), encoding='utf8') as config_file:
        server_options = json.load(config_file)

    for region in regions[:-1]:
        emission = await wrapper.get_emission(region)
        if emission_times[region] != emission['previousStart'] and 'currentStart' in emission:
            emission_times[region] = emission['previousStart']
            emission_datetime = datetime.strptime(emission['currentStart'], '%Y-%m-%dT%H:%M:%SZ')
            emission_timestamp = emission_datetime.replace(tzinfo=timezone.utc).timestamp()
            for server in server_options['servers']:
                if server['region'] == region or server['region'] == 'ALL':
                    channel = bot.get_channel(int(server['alert_channel']))
                    embed = discord.Embed(title="Emission Checker", description=f"A Emission is occurring in: {region}")
                    embed.add_field(name="Start of Emission", value=f"<t:{int(emission_timestamp)}>", inline=True)
                    embed.set_footer(text="Powered by NobleNet")
                    await channel.send(embed=embed)

#Basic are we ready
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    #Loops and sleep time
    #while True:
        #await check_for_emissions()
        #await asyncio.sleep(10)

#Main emisssion command
@bot.command(description="Checks the last emission")
#Gets the region that you want (we love all regions here not just NA)
async def emission(ctx, region: discord.Option(str)):
    #Checks
    #Checks for perms
    if not region.upper() in regions[:-1]:
        embed=discord.Embed(title="Emission Checker", description="Please Enter a Valid Region: RU, EU, NA, SEA")
        await ctx.respond(embed=embed)
        return
    
    #Calls the get_emission function from out wrapper and gives it the users region
    emission = await wrapper.get_emission(region)

    #Fancy date stuff here using UTC time to find the diffrence in time from last the current
    #Could chuck in some time zone conversion here but im lazy
    emission_time = datetime.strptime(emission['previousStart'], '%Y-%m-%dT%H:%M:%SZ')
    time_diffrence = (datetime.utcnow() - emission_time)

    #Getss the hours min sec from the timedelta above
    hours = time_diffrence.seconds // 3600
    minutes = (time_diffrence.seconds % 3600) // 60
    seconds = (time_diffrence.seconds % 3600) % 60
    
    #Just a check to see if hour is 0 and print a diff message dont want it aying 0 hours 10 min just looks sad
    if hours == 0:
        #We love discord embeds
        embed=discord.Embed(title="Emission Checker", description=f"It has been {minutes} Minutes and {seconds} Seconds Since the Last Emission \n Region: {region.upper()}")
        embed.add_field(name="Last Emission", value=f"<t:{int(emission_time.replace(tzinfo=timezone.utc).timestamp())}>", inline=False)
        await ctx.respond(embed=embed)
    else:
        embed=discord.Embed(title="Emission Checker", description=f"It has been {hours} Hours, {minutes} Minutes and {seconds} Seconds Since the Last Emission \n Region: {region.upper()}")
        embed.add_field(name="Last Emission", value=f"<t:{int(emission_time.replace(tzinfo=timezone.utc).timestamp())}>", inline=False)
        await ctx.respond(embed=embed)

@bot.command(description="Sets up what channel the emission should alert to")
#Setups the channel you want to alert in
async def add_alert(ctx, region: discord.Option(str)):
    #Some Presetup
    #sets the region to upper so evnen if eu and EU are enterd its fine
    region = region.upper()

    #Opens the server config as listObj and closes it
    with open('server_config.json') as fp:
        listObj = json.load(fp)

    #Checks
    #Check for permission
    if not ctx.user.guild_permissions.administrator:
        embed=discord.Embed(title="Emission Checker", description="You have no power here")
        await ctx.respond(embed=embed)
        return
    
    #Checks to see if we enterd a propper region
    if not region.upper() in regions:
        embed=discord.Embed(title="Emission Checker", description="Please Enter a Valid Region: RU, EU, NA, SEA, ALL")
        await ctx.respond(embed=embed)
        return

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

    #Create and append the new alert to the listObj and rewrite the server_config file
    listObj['servers'].append({"guild_id": ctx.guild_id,"alert_channel": ctx.channel_id,"region": region})
    with open('server_config.json', 'w') as json_file:
        json.dump(listObj, json_file, indent=4,separators=(',',': '))

    #Send secusses message
    embed=discord.Embed(title="Emission Checker", description=f"The Alert for the {region} region has been added")
    await ctx.respond(embed=embed) 

@bot.command(description="Views the current alerts")
#Setups the channel you want to alert in
async def view_alert(ctx):
    #Setup
    #Open our server_config
    with open('server_config.json') as fp:
        listObj = json.load(fp)

    matching_servers = [server['region'] for server in listObj['servers'] if server['guild_id'] == ctx.guild_id]
    #Checks
    #Check for permission
    if not ctx.user.guild_permissions.administrator:
        embed=discord.Embed(title="Emission Checker", description="You have no power here")
        await ctx.respond(embed=embed)
        return

    #Check to see if the guild has any alerts
    if not matching_servers:
        embed=discord.Embed(title="Emission Checker", description="There not no alerts setup in this channel")
        await ctx.respond(embed=embed)
        return
    
    #Main code prints the guilds alert
    embed=discord.Embed(title="Emission Checker", description="Here are the current alerts for this channel")
    embed.add_field(name="Region:", value='\n'.join(e for e in matching_servers), inline=False)
    await ctx.respond(embed=embed)

@bot.command(description="Remoe a alert from a channel")
async def remove_alert(ctx, region: discord.Option(str)):
    #Setup
    #set the region to upper for convinace 
    region = region.upper()
    #Open our server_config
    with open('server_config.json') as fp:
        listObj = json.load(fp)

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
    with open('server_config.json', 'w') as json_file:
        json.dump(listObj, json_file, indent=4,separators=(',',': '))

    embed=discord.Embed(title="Emission Checker", description=f"The Alert for {region} has been removed")
    await ctx.respond(embed=embed) 

bot.run(auth.token)
#asyncio.get_event_loop().run_until_complete(bot.run(auth.token))
