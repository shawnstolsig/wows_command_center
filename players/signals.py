from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Player
from clans.models import Clan
from clans.utils import get_clan_info

# Whenever a User is created, check to see if there is a Player than can be associated.  If not, create and link one.
@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):

    # if new User is created
    if created:

        # get the User's info, email = wgid and last_name = domain
        wg_player_id = instance.email
        player_domain = instance.last_name

        # get Player from db if already exists, or create a new one for this User
        player, new_player = Player.objects.get_or_create(id=wg_player_id)
        player.user = instance

        # get info from WG API about player's clan
        wg_clan_details = get_clan_info(wg_player_id, player_domain)

        # if player's clan details successfully retrieved
        if wg_clan_details:
            
            # get Clan from db if already exists, or create a new one for this User
            clan, new_clan = Clan.objects.get_or_create(id=wg_clan_details['clan_id'])

            # update clan's name/tag regardless if Clan already existed in db
            clan.name = wg_clan_details['name']
            clan.tag = wg_clan_details['tag']
            clan.save()
            player.clan = clan
        
        # save changes to Player
        player.save()

        if new_player:
            print(f'New player created, {player}')
        else:
            print(f'No new player created, {player}')

        if new_clan:
            print(f'New player created, {clan}')
        else:
            print(f'No new player created, {clan}')

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()