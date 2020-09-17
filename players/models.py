from django.db import models
from django.contrib.auth.models import User

from clans.models import Clan

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    joined_clan_at = models.DateTimeField(blank=True, null=True)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


