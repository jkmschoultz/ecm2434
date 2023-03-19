import math
import json
from database.models import User, UserAchievement, Achievement
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from achievements.views import getAllUserAchievements

##Creates a function for frontend to make a POST request to backend
@csrf_exempt
def index(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        name = str(body_data.get('name'))
        username = str(body_data.get('username'))
        password = str(body_data.get('password'))
        u = User(username = username, name = name, password = password,
            xp = 0, points = 0, has_been_verified = False)
        u.save()

##Function that will verify the account
def verifyAccount(request, username):
    updating_user = User.objects.get(username = username)
    updating_user.has_been_verified = True
    updating_user.save()
    return JsonResponse({})

##Adds xp when a bottle is filled
def bottleFilled(request, current_username):
    updating_user = User.objects.get(username = current_username)
    updating_user.xp = updating_user.xp + 10
    updating_user.save()
    return JsonResponse({})

##Updates the name of a user 
def setName(request, current_username, new_name):
    updating_user = User.objects.get(username = current_username)
    updating_user.name = new_name
    updating_user.save()
    return JsonResponse({})

##Gets data needed to display data for the profile page by returning a json
def getUserProfileData(request, current_username):
    user = User.objects.get(username = current_username)
    name = user.name
    level = int(user.level)
    xpLeft = int(user.xpLeft)
    points = int(user.points)
    email = user.email
    achievement = getAllUserAchievements(current_username)
    return JsonResponse({
        "name":name,
        "username":current_username,
        "level":level,
        "XP":xpLeft,
        "email":email,
        "points": points,
        "achievements": achievement
    })

    


