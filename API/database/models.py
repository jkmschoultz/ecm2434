from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    xp = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    one_time_code = models.CharField(max_length=6)
    has_been_verified = models.BooleanField(default=False)
    
    @property
    def level(self):
        return self.xp / 10

class Building(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
