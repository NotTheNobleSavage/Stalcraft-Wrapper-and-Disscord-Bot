import discord
from discord.ext import commands
from datetime import datetime, timezone
from discord.ui import View, Button
import json
import wrapper

class Clan(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regions = ["RU","EU","NA","SEA","ALL"]


    @discord.slash_command(description="View the current clans")
    #Gets the region that you want (we love all regions here not just NA)
    async def clans(self,ctx,region: discord.Option(str)):

        user = ctx.user
        page = 0

        if not region.upper() in self.regions:
            embed=discord.Embed(title="Stalcraft Clans", description="Please Enter a Valid Region: RU, EU, NA, SEA")
            await ctx.respond(embed=embed)
            return

        clans = await wrapper.get_clan_list(region,0)

        if clans['totalClans'] == 0:
            embed=discord.Embed(title="Stalcraft Clans", description="No Clans Found")
            await ctx.respond(embed=embed)
            return            

        async def button_left(interaction):
            if interaction.user != user:
                await  interaction.response.defer()
            nonlocal page
            if page == 0:
                page = (len(clans['data']) - 1)
            else:
                page = page - 1
            await interaction.response.defer()

        async def button_right(interaction):
            if interaction.user != user:
                await interaction.response.defer()
            nonlocal page
            if page == (len(clans['data']) - 1):
                page = 0
            else:
                page = page + 1
            await interaction.response.defer()

        left = Button(label="Previous Page", style=discord.ButtonStyle.blurple)
        right = Button(label="Next Page", style=discord.ButtonStyle.blurple)

        left.callback = button_left
        right.callback = button_right

        view = View()
        view.add_item(left)
        view.add_item(right)

        embed = discord.Embed(title="Stalcraft Clans",description=f"Name: {clans['data'][page]['name']}")
        embed.add_field(name="Information:", value = f"Name: {clans['data'][page]['name']} \n Members: {clans['data'][page]['memberCount']} \n Clan Tag: {clans['data'][page]['tag']} \n Alliance: {clans['data'][page]['alliance']} \n Description: \n {clans['data'][page]['description']}")   
        embed.set_footer(text=f"Page: {page+1} out of {len(clans['data'])}")
        msg = await ctx.respond(embed=embed,view=view)
        msg = await msg.original_response()

        while True:
            await self.bot.wait_for('interaction', check=lambda interaction: interaction.user == user)
            embed = discord.Embed(title="Stalcraft Clans",description=f"Name: {clans['data'][page]['name']}")
            embed.add_field(name="Information:", value = f"Name: {clans['data'][page]['name']} \n Members: {clans['data'][page]['memberCount']} \n Clan Tag: {clans['data'][page]['tag']} \n Alliance: {clans['data'][page]['alliance']} \n Description: \n {clans['data'][page]['description']}")   
            embed.set_footer(text=f"Page: {page+1} out of {len(clans['data'])}")
            await msg.edit(embed=embed,view=view)

def setup(bot):
    bot.add_cog(Clan(bot))