import discord
from discord.ext import commands
from datetime import datetime, timezone
from discord.ui import View, Button
import json
import wrapper

class Current_Lots(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regions = ["RU","EU","NA","SEA","ALL"]
        self.emission_times = {region: None for region in self.regions}
        self.quality = {0:"Common",1:"Uncommon",2:"Special",3:"Rare",4:"Exclusive",5:"Legendary",6:"Unique"}

    @discord.slash_command(description="Views all the current lots for the item in the region")
    #Gets the region that you want (we love all regions here not just NA)
    async def current_lots(self,ctx, item_name: discord.Option(str),region: discord.Option(str)):

        user = ctx.user
        page = 0

        if not region.upper() in self.regions:
            embed=discord.Embed(title="Stalcraft Market", description="Please Enter a Valid Region: RU, EU, NA, SEA")
            await ctx.respond(embed=embed)
            return

        with open('json/items.json') as fp:
            listObj = json.load(fp)
            for items in listObj['items']:
                if items['item_name'].upper() == item_name.upper():
                    lots = await wrapper.get_auction_lots(region,items['item_id'])
                    lots.update({"item_name": items['item_name'],"item_link" : items['item_link']})

        if not any(item_name in item['item_name'] for item in listObj['items']):
            embed=discord.Embed(title="Stalcraft Market", description="The item you have enterd is invalid")
            await ctx.respond(embed=embed)
            return


        if lots['total'] == 0:
            embed=discord.Embed(title="Stalcraft Market", description="No Lots has been found")
            await ctx.respond(embed=embed)
            return

        async def button_left(interaction):
            if interaction.user == user:
                nonlocal page
                if page == 0:
                    page = (len(lots['lots']) - 1)
                else:
                    page = page - 1
                await interaction.response.defer()
            else:
                await  interaction.response.defer()

        async def button_right(interaction):
            if interaction.user == user:
                nonlocal page
                if page == (len(lots['lots']) - 1):
                    page = 0
                else:
                    page = page + 1
                await interaction.response.defer()
            else:
                await interaction.response.defer()

        left = Button(label="Previous Page", style=discord.ButtonStyle.blurple)
        right = Button(label="Next Page", style=discord.ButtonStyle.blurple)

        left.callback = button_left
        right.callback = button_right

        view = View()
        view.add_item(left)
        view.add_item(right)

        startTime = datetime.strptime(lots['lots'][page]['startTime'], '%Y-%m-%dT%H:%M:%SZ')
        startTime = startTime.replace(tzinfo=timezone.utc).timestamp()

        endTime = datetime.strptime(lots['lots'][page]['endTime'], '%Y-%m-%dT%H:%M:%SZ')
        endTime = endTime.replace(tzinfo=timezone.utc).timestamp()

        embed = discord.Embed(title="Stalcraft Market",description=f"Name: {lots['item_name']}")

        if 'qlt' in lots['lots'][page]['additional'] and 'ptn' in lots['lots'][page]['additional']:
            embed = discord.Embed(title="Stalcraft Market",description=f"Name: {lots['item_name']} + {lots['lots'][page]['additional']['ptn']}")
            embed.add_field(name="Information:", value = f"Quality: {self.quality[lots['lots'][page]['additional']['qlt']]} \n Start Price: {lots['lots'][page]['startPrice']} \n Buyout Price: {lots['lots'][page]['buyoutPrice']} \n Start Time: <t:{int(startTime)}> \n End Time: <t:{int(endTime)}>")   
        elif 'qlt' in lots['lots'][page]['additional']:
            embed.add_field(name="Information:", value = f"Quality: {self.quality[lots['lots'][page]['additional']['qlt']]} \n Start Price: {lots['lots'][page]['startPrice']} \n Buyout Price: {lots['lots'][page]['buyoutPrice']} \n Start Time: <t:{int(startTime)}> \n End Time: <t:{int(endTime)}>")   
        else:
            embed.add_field(name="Information:", value = f"Start Price: {lots['lots'][page]['startPrice']} \n Buyout Price: {lots['lots'][page]['buyoutPrice']} \n Start Time: <t:{int(startTime)}> \n End Time: <t:{int(endTime)}>")
            
        embed.set_footer(text=f"Page: {page+1} out of {len(lots['lots'])}")
        embed.set_thumbnail(url=f"https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/global/{lots['item_link']}")
        msg = await ctx.respond(embed=embed,view=view)
        msg = await msg.original_response()

        while True:
            await self.bot.wait_for('interaction', check=lambda interaction: interaction.user == user)
            #TIME STUFF
            startTime = datetime.strptime(lots['lots'][page]['startTime'], '%Y-%m-%dT%H:%M:%SZ')
            startTime = startTime.replace(tzinfo=timezone.utc).timestamp()

            endTime = datetime.strptime(lots['lots'][page]['endTime'], '%Y-%m-%dT%H:%M:%SZ')
            endTime = endTime.replace(tzinfo=timezone.utc).timestamp()

            embed = discord.Embed(title="Stalcraft Market",description=f"Name: {lots['item_name']}")

            if 'qlt' in lots['lots'][page]['additional'] and 'ptn' in lots['lots'][page]['additional']:
                embed = discord.Embed(title="Stalcraft Market",description=f"Name: {lots['item_name']} + {lots['lots'][page]['additional']['ptn']}")
                embed.add_field(name="Information:", value = f"Quality: {self.quality[lots['lots'][page]['additional']['qlt']]} \n Start Price: {lots['lots'][page]['startPrice']} \n Buyout Price: {lots['lots'][page]['buyoutPrice']} \n Start Time: <t:{int(startTime)}> \n End Time: <t:{int(endTime)}>")   
            elif 'qlt' in lots['lots'][page]['additional']:
                embed.add_field(name="Information:", value = f"Quality: {self.quality[lots['lots'][page]['additional']['qlt']]} \n Start Price: {lots['lots'][page]['startPrice']} \n Buyout Price: {lots['lots'][page]['buyoutPrice']} \n Start Time: <t:{int(startTime)}> \n End Time: <t:{int(endTime)}>")   
            else:
                embed.add_field(name="Information:", value = f"Start Price: {lots['lots'][page]['startPrice']} \n Buyout Price: {lots['lots'][page]['buyoutPrice']} \n Start Time: <t:{int(startTime)}> \n End Time: <t:{int(endTime)}>")
            
            embed.set_footer(text=f"Page: {page+1} out of {len(lots['lots'])}")
            embed.set_thumbnail(url=f"https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/global/{lots['item_link']}")
            await msg.edit(embed=embed,view=view)
def setup(bot):
    bot.add_cog(Current_Lots(bot))