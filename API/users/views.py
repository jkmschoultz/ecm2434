import math
from database.models import User, UserAchievement, Achievement
from django.http import JsonResponse

def UserRef(new_username, new_password):
    u = User(username = new_username, name = new_username, password = new_password,
            xp = 0, points = 0, has_been_verified = False)
    u.save()

def verifyAccount(current_username):
    current_username.has_been_verified = True
    current_username.save()

def bottleFilled(current_username):
    current_username.points = current_username.points + 5
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
    user = User.objects.get(username = current_username)
    user_achievements = list(UserAchievement.objects.filter(user = user))
    data = []
    for achieved in user_achievements:
        data.append(achieved.achievement.challenge)
    level = getUserLevel(current_username)
    xpLeft = getUserXpLeft(current_username)
    return JsonResponse({"username":name, "Level":level, "XP":xpLeft, "streak":0, "Achievments":data})

    
def getUserLevel(current_username):
    xp = int(User.objects.get(username = current_username).xp)
    level = 10*(math.log(1-((xp*(1-(2**(1/10))))/10) ,2))
    level = int(level)
    return level

def getUserXpLeft(current_username):
    xp = User.objects.get(username = current_username).xp
    level = 10*(math.log(1-((xp*(1-(2**(1/10))))/10) ,2))
    level = int(level)
    xp_left = xp - ((10*(1-(2**(level/10)))) / (1-(2**(1/10))))
    xp_left = int(xp_left) + 1
    return xp_left

def getPoints(current_username):
    points = User.objects.get(username = current_username).password
    return points

    


