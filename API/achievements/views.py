import math
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database.models import UserAchievement,User,Achievement



def detail(request, current_username):
    totalFilledBottlesAchievementCheck(current_username)
    return JsonResponse({})

def totalFilledBottlesAchievementCheck(current_username):
    user = User.objects.get(username = current_username)
    bottles = user.bottles
    listOfAchievements = UserAchievement.objects.all()
    listOfBottleCheckpoints = [1,5,10,50,100,250,500,1000]

    for checkpoint in listOfBottleCheckpoints:
        if bottles >= checkpoint:
            if checkpoint == 1:
                challenge = "Fill up your first water bottle"
            else:
                challenge = "Fill up " + str(checkpoint) + " bottles"

            achievement = Achievement.objects.get(challenge = challenge)
            try:
                UserAchievement.objects.get(user = user, achievement = achievement)
            except:
                newUserAchievement = UserAchievement.objects.create(
                    user = user,
                    achievement = achievement)
            
                user.xp = user.xp + achievement.xp_reward
                user.points = user.points + achievement.points_reward
                user.save()
