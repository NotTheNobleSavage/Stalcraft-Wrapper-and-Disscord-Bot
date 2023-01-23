#WE USE PYCORD HERE NOT DISCORD.PY
import discord

#Auth and Wrapper
import auth
import wrapper

#Python modules
from datetime import datetime
bot = discord.Bot()

#Basic are we ready
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

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
            embed=discord.Embed(title="Emission Checker", description="It has been "+str(minutes)+" Minutes and "+str(seconds)+" Seconds Since the Last Emission")
            embed.add_field(name="Last Emission", value=str(emission_time), inline=False)
            await ctx.respond(embed=embed)
        else:
            embed=discord.Embed(title="Emission Checker", description="It has been "+str(hours)+" Hours, "+str(minutes)+" Minutes and "+str(seconds)+" Seconds Since the Last Emission")
            embed.add_field(name="Last Emission", value=str(emission_time) + " (UTC) ", inline=False)
            await ctx.respond(embed=embed)
    else:
        #Remember that region check yea this is where we tell the user
        embed=discord.Embed(title="Emission Checker", description="Please Enter a Valid Region: RU, EU, NA, SEA")
        await ctx.respond(embed=embed)        

#oh and we gotta run the bot i nearly forgot
bot.run(auth.token)

