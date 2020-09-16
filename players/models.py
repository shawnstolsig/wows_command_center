from django.db import models
from django.contrib.auth.models import User

from clans.models import Clan

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, blank=True, null=True)

