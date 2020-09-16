from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from clans.models import Clan

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, blank=True, null=True)


# Whenever a User is created, check to see if there is a Player than can be associated.  If not, create and link one.
@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        player, new_player = Player.objects.get_or_create(id=instance.email)
        player.user = instance
        player.save()
        if new_player:
            print(f'New player created, {player}')
        else:
            print(f'No new player created, {player}')

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()