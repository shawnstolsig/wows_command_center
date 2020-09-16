from django.db import models

class Clan(models.Model):
    tag = models.CharField(max_length=10)
    name = models.CharField(max_length=100)