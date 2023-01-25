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
regions = ['RU',"EU","NA","SEA"]
previous_emission = {region: None for region in regions}
with open(os.path.normpath('server_config.json'), encoding='utf8') as f:
    server_options = json.load(f)
async def check_for_emission():
    #We love all regions
    for region in regions:
        emission = wrapper.get_emission(region)
        if previous_emission[region] != emission['previousStart'] and 'currentStart' in emission:
            previous_emission[region] = emission['previousStart']
            emission_time = datetime.strptime(emission['previousStart'], '%Y-%m-%dT%H:%M:%SZ')
            emission_time = emission_time.replace(tzinfo=timezone.utc).timestamp()
            emission_time = int(emission_time)
            for server in [s for s in server_options['servers'] if s['region'] == region or s['region'] == 'all']:
                channel = bot.get_channel(int(server['alert_channel']))
                embed=discord.Embed(title="Emission Checker", description=f"A Emission is occurring in: \n {region}")
                embed.add_field(name="Start of Emission", value=f"<t:{emission_time}>", inline=True)
                embed.set_footer(text="Powerd by NobleNet ")
                await channel.send(embed=embed)
#Basic are we ready
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    #Loops and sleep time
    while True:
        await check_for_emission()
        await asyncio.sleep(10)

#Main emisssion command
@bot.command(description="Checks the last emission")
#Gets the region that you want (we love all regions here not just NA)
async def emission(ctx, region: discord.Option(str)):
    #Quick check did you give a region we know of (will change with more servers getting added in)
    if region == "RU" or region == "EU" or region == "NA" or region == "SEA":
        #Calls the get_emission function from out wrapper and gives it the users region
        emission = wrapper.get_emission(region)

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
            embed=discord.Embed(title="Emission Checker", description=f"It has been {minutes} Minutes and {seconds} Seconds Since the Last Emission \n Region: {region}")
            embed.add_field(name="Last Emission", value=f"<t:{int(emission_time.replace(tzinfo=timezone.utc).timestamp())}>", inline=False)
            await ctx.respond(embed=embed)
        else:
            embed=discord.Embed(title="Emission Checker", description=f"It has been {hours} Hours, {minutes} Minutes and {seconds} Seconds Since the Last Emission \n Region: {region}")
            embed.add_field(name="Last Emission", value=f"<t:{int(emission_time.replace(tzinfo=timezone.utc).timestamp())}>", inline=False)
            await ctx.respond(embed=embed)
    else:
        #Remember that region check yea this is where we tell the user
        embed=discord.Embed(title="Emission Checker", description="Please Enter a Valid Region: RU, EU, NA, SEA")
        await ctx.respond(embed=embed)        

#oh and we gotta run the bot i nearly forgot
bot.run(auth.token)

