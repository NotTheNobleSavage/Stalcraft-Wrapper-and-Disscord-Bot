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
        ** /remove_alert region: ** \n This command is used to remove an alert for region specified in the current channel. \n
        ** /help ** \n This can be used to run this command and view help info.\n
        ** /clans region: ** \n Used to view all the clans in the current regions, only works in RU right now. \n
        ** /current_lots item_name:, region: ** \n Can be used to find the current auctions for the item specified in the region. \n
        ** /get_player region: player_name: ** \n Is used to view stats about a player.
        ** /players_compare region:, player_name:, region2:, player_name2:, ** \n Used to compare 2 different players.
        """)
        await ctx.respond(embed=embed)
        return            

def setup(bot):
    bot.add_cog(Help(bot))
