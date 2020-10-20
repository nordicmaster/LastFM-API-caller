from django.db import models


class StatsArtist(models.Model):
    artist = models.CharField(max_length=65)
    listeners = models.IntegerField()
    scrobbles = models.IntegerField()
    ratio = models.FloatField()
    last_seen = models.DateField()
