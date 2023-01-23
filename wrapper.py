#The Request module
import requests

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
def get_regions():
    url = 'https://eapi.stalcraft.net/regions'
    response = requests.get(url)
    response = response.json()
    return response

#Again returns a Json Object with the history of an item_id you give it https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1auction~1%7Bitem%7D~1history/get
#Can be giving extra query params such as offset and limit 
def get_auction_history(region,item_id):
    url = f'https://eapi.stalcraft.net/{region}/auction/{item_id}/history'
    headers = {"Authorization": f"Bearer {AppAuth}"}
    response = requests.get(url, headers=headers)
    response = response.json()
    return response

#Gets the current lots of an item and gives back a Json Object https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1auction~1%7Bitem%7D~1lots/get
def get_auction_lots(region,item_id):
    url = f'https://eapi.stalcraft.net/{region}/auction/{item_id}/lots'
    headers = {"Authorization": f"Bearer {AppAuth}"}
    response = requests.get(url, headers=headers)
    response = response.json()
    return response

#Give a Json Object of the past emission (if an emisssion is currently happerning will also give a currentStart value can be used to check if one is happening) https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1emission/get
def get_emission(region):
    url = f'https://eapi.stalcraft.net/{region}/emission'
    headers = {"Authorization": f"Bearer {AppAuth}"}
    response = requests.get(url, headers=headers)
    response = response.json()
    return response

#Clans have not been implemented in any server other then RU but returns info about a clan using the clan id https://eapi.stalcraft.net/reference#/paths/~1%7Bregion%7D~1clan~1%7Bclan-id%7D~1info/get
def get_clan_info(region,clan_id):
    url = f'https://eapi.stalcraft.net/{region}/clan/{clan_id}/info'
    headers = {"Authorization": f"Bearer {AppAuth}"}
    response = requests.get(url, headers=headers)
    response = response.json()
    return response

#Lists all the clans in a region and again returns a Json Object
def get_clan_list(region):
    url = f'https://eapi.stalcraft.net/{region}/clans'
    headers = {"Authorization": f"Bearer {AppAuth}"}
    response = requests.get(url, headers=headers)
    response = response.json()
    return response

#Sorry i have no clue how to get my UserAuth for some reason steam logging bugs it out but using the above code you can add it down here if you want
