from django.db import models

class Clan(models.Model):
    
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    members_count = models.IntegerField(default=0)
    
    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
