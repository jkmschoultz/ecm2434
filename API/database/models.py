from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import math

# Define database models here
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )
        return self.create_user(username, email, password, **other_fields)
    
    def create_user(self, username, email, password, **other_fields):
        if not username:
            raise ValueError('Must provide a username')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=30, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    xp = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    bottles = models.PositiveIntegerField(default=0)
    one_time_code = models.CharField(max_length=6, default=123456)
    has_been_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    @property
    def level(self):
        return int(10*(math.log(1-((self.xp*(1-(2**(1/10))))/10) ,2)))
    
    @property
    def xpLeft(self):
        return int(self.xp - ((10*(1-(2**(self.level/10)))) / (1-(2**(1/10)))))
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username

class Building(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    image = models.ImageField(blank=True)
    
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
        return self.user.username + ', ' + self.question.text

class Leaderboard(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_points_in_building = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.building.name + ', ' + self.user.username + ', ' + str(self.user_points_in_building)

class Achievement(models.Model):
    name = models.CharField(max_length=255, default="")
    challenge = models.CharField(max_length=255)
    xp_reward = models.PositiveIntegerField()
    points_reward = models.PositiveIntegerField()
    
    def __str__(self):
        return self.challenge

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username + ', ' + self.achievement.challenge

class Fountain(models.Model):
    location = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.building.name + ', ' + self.location
