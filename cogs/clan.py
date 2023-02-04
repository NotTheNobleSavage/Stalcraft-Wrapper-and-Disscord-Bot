import discord
from discord.ext import commands
from datetime import datetime, timezone
from discord.ui import View, Button
from discord.ext import commands, pages
import json
import wrapper

class Clan(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regions = ["RU","EU","NA","SEA","ALL"]

    clan_command_group = discord.SlashCommandGroup("clan", "clan related commands")

    def get_pages(self,clans):
        pages = []
        for clan in clans['data']:
            embed = discord.Embed(title="Stalcraft Clans",description=f"Name: {clan['name']}")
            embed.add_field(name="Information:", value = f"""
            Members: {clan.get('memberCount',"Unknown")}
            Clan Tag: {clan.get('tag',"Unknown")}
            Alliance: {clan.get('alliance',"Unknown")}
            Description:{clan.get('description',"Unknown")}
            """)   
            pages.append(embed)
        
        return pages

    @clan_command_group.command(description="List all current clans")
    async def list(self, ctx: discord.ApplicationContext, region: discord.Option(str, choice = ["RU","SEA","NA","EU"])):

        clans = await wrapper.get_clan_list(region,0)
        if clans['totalClans'] == 0:
            embed=discord.Embed(title="Stalcraft Clans", description="No Clans Found")
            await ctx.respond(embed=embed)
            return 
      
        paginator = pages.Paginator(pages=self.get_pages(clans), loop_pages=True)
        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot):
    bot.add_cog(Clan(bot))