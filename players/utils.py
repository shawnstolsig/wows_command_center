import os
import requests
from datetime import datetime
from django.utils.timezone import make_aware

from .models import Player

def get_player_info(wg_player_id, domain):
    """
    "   Given the user's id, returns basic clan info from WG API
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
    
    # if player was found, return their clan info
    return player_json['data'][str(wg_player_id)]

def create_or_update_player_entry(player_info):
    '''
    '   Takes in detailed clan info from WG's API and either creates or updates the Clan in the db
    '''

    # create a timezone aware datetime object out for joined_clan_at
    join_date = datetime.fromtimestamp(player_info['joined_at'])
    aware_date = make_aware(join_date)

    # get Clan from db if already exists, or create a new one for this User
    player, new_player = Player.objects.get_or_create(id=player_info['account_id'])

    # update clan's name/tag regardless if Clan already existed in db
    player.name = player_info['account_name']
    player.role = player_info['role']
    player.joined_clan_at = aware_date
    player.save()

    return player