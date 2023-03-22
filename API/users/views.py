import math
import json
from database.models import User, FilledBottle, Building, UserItem, ShopItem, Leaderboard
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from achievements.views import getAllUserAchievements, totalFilledBottlesAchievementCheck, \
                buildingAchievementsCheck, streakAchievementsCheck
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import datetime
from django.utils import timezone
import pytz

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

##Adds xp when a valid bottle is filled
def bottleFilled(request, current_username, building_name):
    updating_user = User.objects.get(username = current_username)

    # if user has filled a bottle in the last 10 minutes don't let them fill again
    time = datetime.datetime.now(pytz.utc)
    endTime = time
    startTime = time - datetime.timedelta(minutes=10)
    relevantBottles = FilledBottle.objects.filter(user=updating_user,day__range=(startTime, endTime)).values()

    # return the time left until the user is allowed to track another filled bottle
    if relevantBottles.count() > 0:
        lastBottle = relevantBottles.last().get("day")
        timeRemaining = datetime.timedelta(minutes = 10) - (time - lastBottle)
        return JsonResponse({"data" : {"minutes" : timeRemaining.seconds // 60,
                                        "seconds" : timeRemaining.seconds % 60}})

    # create a record of the user filling a bottle
    time = datetime.datetime.now(pytz.utc)
    building = Building.objects.get(name=building_name)
    FilledBottle.objects.create(user=updating_user, 
                               building=building,
                                day=time)

    updating_user.xp = updating_user.xp + 10
    updating_user.bottles += 1
    updating_user.save()
    # Add user to leaderboard for building
    leaderboard, created = Leaderboard.objects.get_or_create(building=building, user=updating_user)
    leaderboard.user_points_in_building += 10
    leaderboard.save()
    # Check whether user reached any new achievements
    achievements = {"data" : []}
    totalFilledBottlesAchievementCheck(current_username, achievements)
    buildingAchievementsCheck(current_username, achievements)
    streakAchievementsCheck(current_username, achievements)
    # Redirect to get quiz questions once bottle filled
    return redirect('questions:questions')

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
    profile_pic = user.profile_pic.image
    profile_border = user.profile_border.image
    profile_background = user.profile_background.image
    bottles_filled = user.bottles
    achievement = getAllUserAchievements(current_username)
    return JsonResponse({
        "name":name,
        "username":current_username,
        "level":level,
        "XP":xpLeft,
        "email":email,
        "points": points,
        "achievements": achievement,
        "profile_pic": settings.BASE_URL + profile_pic.url,
        "profile_border": settings.BASE_URL + profile_border.url,
        "profile_background": settings.BASE_URL + profile_background.url,
        "bottles_filled": bottles_filled
    })

## Function that sets the pictures of a user
class SetUserPic(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, name, type):
        user = request.user
        # Checks the type of the image change
        if type == 'Profile Picture':
            # Checks to see if the image exists and if the user owns it
            item = get_object_or_404(ShopItem, name = name)
            get_object_or_404(UserItem, item = item, user=user)
            user.profile_pic = item
            user.save()
            return JsonResponse({'changed': type})
        elif type == 'Border':
            # Checks to see if the image exists and if the user owns it
            item = get_object_or_404(ShopItem, name = name)
            get_object_or_404(UserItem, item = item, user=user)
            user.profile_border = item
            user.save()
            return JsonResponse({'changed': type})
        elif type == 'Background':
            # Checks to see if the image exists and if the user owns it
            item = get_object_or_404(ShopItem, name = name)
            get_object_or_404(UserItem, item = item, user=user)
            user.profile_background = item
            user.save()
            return JsonResponse({'changed': type})
        else:
            return HttpResponseBadRequest('Must specify item type')

class AuthGetUserData(APIView):
    # Redirect to get profile data for an authorised user
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get username of authenticated user and redirect
        user = request.user
        return redirect('users:getUserProfileData', current_username=user.username)
