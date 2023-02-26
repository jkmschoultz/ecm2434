import math
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database.models import UserAchievement,User,Achievement



def detail(request, current_username):
    totalFilledBottlesAchievementCheck(current_username)
    return JsonResponse({})

def totalFilledBottlesAchievementCheck(current_username):
    bottles = User.objects.get(username = current_username).bottles
    listOfAchievements = UserAchievement.objects.all()

    #Fill up your first bottle
    if bottles >= 1:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up your first water bottle"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 25
        user.points = user.points + 5
        user.save()

    #Fill up 5 bottles
    if bottles >= 5:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 5 bottles"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 20
        user.points = user.points + 3
        user.save()

    #Fill up 10 bottles
    if bottles >= 10:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 10 bottles"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 30
        user.points = user.points + 3
        user.save()


    #Fill up 50 bottles
    if bottles >= 50:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 50 bottles"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 50
        user.points = user.points + 5
        user.save()

    
    #Fill up 100 bottles
    if bottles >= 100:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 100 bottles"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 75
        user.points = user.points + 5
        user.save()


    #Fill up 250 bottles
    if bottles >= 250:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 250 bottles"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 100
        user.points = user.points + 10
        user.save()


    #Fill up 500 bottles
    if bottles >= 500:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 500 bottles"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 200
        user.points = user.points + 15
        user.save()


    #Fill up 1000 bottles
    if bottles >= 1000:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 1000 bottles"))
        
        user = User.objects.get(username = current_username)
        user.xp = user.xp + 300
        user.points = user.points + 25
        user.save()

