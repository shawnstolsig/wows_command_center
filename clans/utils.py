import os
import requests

def get_clan_info(wg_player_id, domain):
    """
    "   Gets detailed clan information whenever a User is created by querying the WG API.
    "   First, gets the player's clan, then gets that clan's detailed information.  
    "   Return None if unable to reach the WG API or if there are any other issues identifying
    "   the User's clan.
    """
        
    # get set WG_APP_ID from environment variables
    WG_APP_ID = os.getenv("WG_APP_ID")

    # pull player clan details from WG API
    url = f'https://api.worldofwarships.{domain}/wows/clans/accountinfo/?application_id={WG_APP_ID}&account_id={wg_player_id}'
    response = requests.get(url)

    # if invalid response from WG, abort
    if response.status_code != 200:
        return None
    
    # convert response to JSON
    player_json = response.json()

    # if player wasn't found, or more than one was found
    if player_json['status'] != 'ok':
        return None
    elif player_json['meta']['count'] != 1:
        return None
    
    # if player was found, get clan ID
    clan_id = player_json['data'][str(wg_player_id)]['clan_id']

    # get clan info 
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

    # return the detailed clan info.  keys: name, tag, members_count, members_ids, description, leader_name
    return clan_json['data'][str(clan_id)]
