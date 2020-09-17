from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Player
from clans.models import Clan
from .utils import get_player_info, create_or_update_player_entry
from clans.utils import get_clan_info, create_or_update_clan_entry

# Whenever a User is created, check to see if there is a Player than can be associated.  If not, create and link one.
@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    """
    "   This function is invoked whenever a new User is created.  Gets or Creates (and subsequently links)
    "   the User, Player, and Clan models. Note that 'instance' is the User that was just created.
    """

    # if new User is created
    if created:

        # get the user's domain from last_name
        domain = instance.last_name

        # get Player info from WG's database 
        player_info = get_player_info(instance.id, domain)

        # if successfully found player info
        if player_info:

            # write Player info to database
            player = create_or_update_player_entry(player_info)
            instance.player = player   

            # if the player has a clan
            if player_info['clan_id']:
                # get info from WG API about player's clan
                clan_info = get_clan_info(player_info['clan_id'], domain)

                # if player's clan details successfully retrieved
                if clan_info:

                    # attach the Clan to the Player
                    clan = create_or_update_clan_entry(clan_info)
                    player.clan = clan
                else: 
                    print(f'Unable to find clan_info in players.signals')
            else: 
                print(f'Player is not in a clan.')

            # save changes to Player
            player.save()
        else: 
            print(f'Unable to find player_info in players.signals')

        # save changes to the User instance
        instance.save()

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()