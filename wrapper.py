#The Request module
import aiohttp
import asyncio
import requests
import json

#Auth file containing the client_id and client_secret (this should be provided by the telegram bot)
import auth

#This is usesd to get the AppAuth Authentication Token we just run this whenever the script is called and get a new token
def get_appauth_token(client_id, client_secret):
    url = 'https://exbo.net/oauth/token'
    headers = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}
    response = requests.post(url , json=headers)
    response = response.json()
    return(response['access_token'])

#This just runs the above code with the credential in the auth file 
AppAuth = get_appauth_token(auth.client_id,auth.client_secret)



#Just returns a Json Object with all the regions avalible no auth iss requied https://eapi.stalcraft.net/reference#/paths/~1regions/get
async def get_regions():
    async with aiohttp.ClientSession() as session:
        url = 'https://eapi.stalcraft.net/regions'
        async with session.get(url) as response:
            response = await response.json()
        return response
#Again returns a Json Object with the history of an item_id you give it https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1auction~1%7Bitem%7D~1history/get
#Can be giving extra query params such as offset and limit 
async def get_auction_history(region,item_id):
    async with aiohttp.ClientSession() as session:
        url = f'https://eapi.stalcraft.net/{region}/auction/{item_id}/history'
        async with session.get(url, headers = {"Authorization": f"Bearer {AppAuth}"}) as response:
            response = await response.json()
        return response
#Gets the current lots of an item and gives back a Json Object https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1auction~1%7Bitem%7D~1lots/get
async def get_auction_lots(region,item_id):
    async with aiohttp.ClientSession() as session:
        url = f'https://eapi.stalcraft.net/{region}/auction/{item_id}/lots?additional=true'
        async with session.get(url, headers = {"Authorization": f"Bearer {AppAuth}"}) as response:
            response = await response.json()
        return response
#Give a Json Object of the past emission (if an emisssion is currently happerning will also give a currentStart value can be used to check if one is happening) https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1emission/get
async def get_emission(region):
    async with aiohttp.ClientSession() as session:
        url = f'https://eapi.stalcraft.net/{region}/emission'
        async with session.get(url, headers = {"Authorization": f"Bearer {AppAuth}"}) as response:
            response = await response.json()
        return response
#Clans have not been implemented in any server other then RU but returns info about a clan using the clan id https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1clan~1%7Bclan-id%7D~1info/get
async def get_clan_info(region,clan_id):
    async with aiohttp.ClientSession() as session:
        url = f'https://eapi.stalcraft.net/{region}/clan/{clan_id}/info'
        async with session.get(url, headers = {"Authorization": f"Bearer {AppAuth}"}) as response:
            response = await response.json()
        return response
#Lists all the clans in a region and again returns a Json Object
async def get_clan_list(region):
    async with aiohttp.ClientSession() as session:
        url = f'https://eapi.stalcraft.net/{region}/clans'
        async with session.get(url, headers = {"Authorization": f"Bearer {AppAuth}"}) as response:
            response = await response.json()
        return response

async def get_player_profile(region,character):
    async with aiohttp.ClientSession() as session:
        url = f'https://eapi.stalcraft.net/{region}/character/by-name/{character}/profile'
        async with session.get(url, headers = {"Authorization": f"Bearer {AppAuth}"}) as response:
            response = await response.json()
        return response
#Sorry i have no clue how to get my UserAuth for some reason steam logging bugs it out but using the above code you can add it down here if you want
