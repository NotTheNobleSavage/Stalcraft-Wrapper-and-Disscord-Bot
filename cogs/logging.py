import discord
from discord.ext import commands
from datetime import datetime, timezone
import json
import os

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction): # this is called when a member joins the server     
        if interaction.type == discord.InteractionType.application_command:
            with open('json/server_logs.json') as fp:
                listObj = json.load(fp)

            listObj['logs'].append({
                "guild_id": interaction.guild.id,
                "guild_name": str(interaction.guild),
                "channel_id": interaction.channel_id,
                "user_id": str(interaction.user),
                "command_data": interaction.data,
                "time_run": str(datetime.now())
            })

            with open('json/server_logs.json', 'w') as json_file:
                json.dump(listObj, json_file, indent=4,separators=(',',': '))

def setup(bot):
    bot.add_cog(Logging(bot))