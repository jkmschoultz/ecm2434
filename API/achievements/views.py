import math
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database.models import UserAchievement,User,Achievement



def detail(request, current_username):

    bottles = User.objects.get(username = current_username).bottles
    listOfAchievements = UserAchievement.objects.all()

    #Fill up your first bottle
    if bottles >= 1:
        print(User.objects.get(username = current_username).id)
        print(Achievement.objects.get(challenge = "Fill up your first water bottle").id)

        newUserAchievement = UserAchievement.objects.create(
            user = User.objects.get(username = current_username),
            achievement =Achievement.objects.get(challenge = "Fill up your first water bottle"))
        print(newUserAchievement)
        return JsonResponse({})