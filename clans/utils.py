import os
import requests

from players.utils import get_player_info, create_or_update_player_entry
from .models import Clan

def refresh_clan_on_login(clan_id, domain):
    """
    "   Upon user login, this function refreshes all of the clan data for that user's clan.
    """

    # get clan info
    clan_info = get_clan_info(clan_id, domain)

    # if successfully retrieved clan info from WG API:
    if clan_info:

        # update the clan info on backend
        clan = create_or_update_clan_entry(clan_info)

        # iterate through all players in clan
        for player_id in clan_info['members_ids']:

            # get that player's info from WG API
            player_info = get_player_info(player_id, domain)
            
            # if successful...
            if player_info:
                # ...post to db
                player = create_or_update_player_entry(player_info)
                player.clan = clan
                player.save()

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

    # return the detailed clan info.  keys: name, tag, clan_id, members_count, description, members_ids
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
    clan.description = clan_info['description']
    clan.members_count = clan_info['members_count']
    clan.save()

    return clan