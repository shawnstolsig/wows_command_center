import os
import requests

from players.utils import get_player_info
from .models import Clan

def get_clan_info(clan_id, domain):
    """
    "   This function takes in a clan's id and domain and gets detailed clan info. 
    """
    # get set WG_APP_ID from environment variables
    WG_APP_ID = os.getenv("WG_APP_ID")
    
    # get detailed clan info 
    url = f'https://api.worldofwarships.{domain}/wows/clans/info/?application_id={WG_APP_ID}&clan_id={clan_id}'
    response = requests.get(url)

    # if invalid response from WG, abort
    if response.status_code != 200:
        return None

    # convert response to JSON
    clan_json = response.json()

    # if clan wasn't found, or more than one was found
    if clan_json['status'] != 'ok':
        return None
    elif clan_json['meta']['count'] != 1:
        return None

    # return the detailed clan info.  
    return clan_json['data'][str(clan_id)]

def create_or_update_clan_entry(clan_info):
    '''
    '   Takes in detailed clan info from WG's API and either creates or updates the Clan in the db
    '''
    # get Clan from db if already exists, or create a new one for this User
    clan, new_clan = Clan.objects.get_or_create(id=clan_info['clan_id'])

    # update clan's name/tag regardless if Clan already existed in db
    clan.name = clan_info['name']
    clan.tag = clan_info['tag']
    clan.save()

    return clan