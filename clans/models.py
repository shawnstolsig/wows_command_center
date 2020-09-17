from django.db import models

class Clan(models.Model):
    
    tag = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
