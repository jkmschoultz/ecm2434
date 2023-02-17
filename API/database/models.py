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

class Question(models.Model):
    question = models.CharField(max_length=255)

class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

class HasAnswered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)

class Leaderboard(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_points_in_building = models.PositiveIntegerField()

class Achievement(models.Model):
    challenge = models.CharField(max_length=255)
    xp_reward = models.PositiveIntegerField()
    points_reward = models.PositiveIntegerField()

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

class Fountain(models.Model):
    location = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
