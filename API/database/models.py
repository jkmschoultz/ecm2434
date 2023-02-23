from django.db import models

# Define database models here
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    xp = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    one_time_code = models.CharField(max_length=6)
    has_been_verified = models.BooleanField(default=False)
    
    @property
    def level(self):
        return self.xp / 10
    
    def __str__(self):
        return self.username

class Building(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    
    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    
    def __str__(self):
        return self.text

class HasAnswered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user.name + ', ' + self.question.text

class Leaderboard(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_points_in_building = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.building.name + ', ' + self.user.name + ', ' + str(self.user_points_in_building)

class Achievement(models.Model):
    challenge = models.CharField(max_length=255)
    xp_reward = models.PositiveIntegerField()
    points_reward = models.PositiveIntegerField()
    
    def __str__(self):
        return self.challenge

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.name + ', ' + self.achievement.challenge

class Fountain(models.Model):
    location = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.building.name + ', ' + self.location
