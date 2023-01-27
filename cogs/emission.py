import discord
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime, timezone
import wrapper

regions = ["RU","EU","NA","SEA","ALL"]

class Emission(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Checks the last emission")
    #Gets the region that you want (we love all regions here not just NA)
    async def emission(self, ctx, region: discord.Option(str)):
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


def setup(bot):
    bot.add_cog(Emission(bot))