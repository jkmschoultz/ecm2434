import math
from database.models import User, UserAchievement, Achievement
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from achievements.views import getAllUserAchievements

'''@csrf_exempt
def index(request):
    print("here the request")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
##        name = str(body_data.get('name'))
##        username = str(body_data.get('username'))
##        password = str(body_data.get('password'))
        name 

        print(name)
        print(username)
        u = User(username = username, name = name, password = password,
            xp = 0, points = 0, has_been_verified = False)
        u.save()
'''
def UserRef(new_username, new_password):
    u = User(username = new_username, name = new_username, password = new_password,
            xp = 0, points = 0, has_been_verified = False)
    u.save()

def verifyAccount(current_username):
    current_username.has_been_verified = True
    current_username.save()

def bottleFilled(current_username):
    current_username.xp = current_username.xp + 10
    current_username.save()

def setName(current_username, changed_name):
    updating_user = User.objects.get(username = current_username)
    updating_user.name = changed_name
    updating_user.save()

def getName(request,username):
    name = User.objects.get(username = username).name
    return JsonResponse({username:name})

def getPassword(current_username):
    password = User.objects.get(username = current_username).password
    return password

def getUserProfileData(request, current_username):
    name = User.objects.get(username = current_username).name
    level = int(User.objects.get(username = current_username).level)
    xpLeft = int(User.objects.get(username = current_username).xpLeft)
    points = User.objects.get(username = current_username).points
    achievement = getAllUserAchievements(current_username)
    return JsonResponse({"name":name, "Level":level, "XP":xpLeft, "streak":0, "points": points, "achievements": achievement})

    


