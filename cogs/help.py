import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Displays all the commands and some info")
    async def help(self, ctx):
        embed=discord.Embed(title="Help", description=f"""
        ** /emission region ** : \n This will allow you to view when the last emission happened in the region of choice. \n
        The features below deal with how you want to be alerted when an emission occurs. These commands can only be run by admins! \n
        ** /add_alert region: ** \n This creates an alert for the region in the current channel in which the command is run. You can set the region to a specific region or can enter “all” to get alerts for all regions. \n
        ** /view_alert: ** \n This views all the current alerts that are set up in this channel. \n
        ** /remove_alert region: ** \n This command is used to remove an alert for region specified in the current channel.
        """)
        await ctx.respond(embed=embed)
        return            

def setup(bot):
    bot.add_cog(Help(bot))