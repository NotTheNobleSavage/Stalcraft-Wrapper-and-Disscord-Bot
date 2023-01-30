import discord
import auth
import json

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_guild_join(guild):
    with open('json/server_list.json') as fp:
        listObj = json.load(fp)

    if not {"guild_id": guild.id,"guild_name": guild.name,"owner_id": guild.owner_id} in listObj['servers']:
        listObj['servers'].append({"guild_id": guild.id,"guild_name": guild.name,"owner_id": guild.owner_id})
        with open('json/server_list.json', 'w') as json_file:
            json.dump(listObj, json_file, indent=4,separators=(',',': '))

cogs_list = [
    'emission',
    'emission_checker',
    'alerts',
    'logging',
    'help',
    'current_lots',
    'clan',
    'player',
    'player_compare'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}',store=False)
bot.run(auth.token)
