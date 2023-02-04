import discord
from discord.ext import commands
from datetime import datetime, timezone
from discord.ui import View, Button
from discord.ext import commands, pages
import json
import wrapper

class Current_Lots(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regions = ["RU","EU","NA","SEA","ALL"]
        self.emission_times = {region: None for region in self.regions}
        self.quality = {0:"Common",1:"Uncommon",2:"Special",3:"Rare",4:"Exclusive",5:"Legendary",6:"Unique"}

    def get_pages(self,lots,item_name,matched_items):
        pages = []
        for lot in lots['lots']:
            startTime = datetime.strptime(lot['startTime'], '%Y-%m-%dT%H:%M:%SZ')
            startTime = startTime.replace(tzinfo=timezone.utc).timestamp()

            endTime = datetime.strptime(lot['endTime'], '%Y-%m-%dT%H:%M:%SZ')
            endTime = endTime.replace(tzinfo=timezone.utc).timestamp()

            embed = discord.Embed(title="Stalcraft Market",description=f"Name: {item_name+' +'+str(lot['additional'].get('ptn')) if lot['additional'].get('ptn') else item_name}")
            embed.add_field(name="Information:", value = f"""
            Quality: {self.quality[lot.get('qlt',0)]}
            Start Price: {lot['startPrice']}
            Buyout Price: {lot['buyoutPrice']}
            Start Time: <t:{int(startTime)}>
            End Time: <t:{int(endTime)}>
            """)
            embed.set_thumbnail(url=f"https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/global/{matched_items[0]['icon']}")
            pages.append(embed)
        
        return pages

    @discord.slash_command(description="Views all the current lots for the item in the region")
    #Gets the region that you want (we love all regions here not just NA)
    async def current_lots(self,ctx, item_name: discord.Option(str),region: discord.Option(str, choice = ["RU","SEA","NA","EU"])):

        with open('json/items.json', encoding='utf8') as fp:
            listObj = json.load(fp)
        matched_items = [item for item in listObj if item_name.upper() in item["name"]["lines"]["ru"].upper() or item_name.upper() in item["name"]["lines"]["en"].upper()]

        item_id = matched_items[0]['data'].split("/")[-1][:-5]

        lots = await wrapper.get_auction_lots(region,item_id)

        paginator = pages.Paginator(pages=self.get_pages(lots,item_name,matched_items), loop_pages=True)
        await paginator.respond(ctx.interaction, ephemeral=False)
def setup(bot):
    bot.add_cog(Current_Lots(bot))