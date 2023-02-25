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
        
    
    #Fill up 5 bottles
    if bottles >= 5:

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up 5 bottles"))

    #Fill up 10 bottles


    #Fill up 50 bottles

    
    #Fill up 100 bottles


    #Fill up 250 bottles


    #Fill up 500 bottles


    #Fill up 1000 bottles

