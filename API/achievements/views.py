import math
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database.models import UserAchievement,User,Achievement, FilledBottle, Building



def detail(request, current_username):
    dictOfNewAchievements = {"data" : []}
    dictOfNewAchievements = totalFilledBottlesAchievementCheck(current_username, dictOfNewAchievements)
    dictOfNewAchievements = buildingAchievementsCheck(current_username, dictOfNewAchievements)
    return JsonResponse(dictOfNewAchievements)

def all(request, current_username):
    dictOfAchievements = getAllUserAchievements(current_username)
    return JsonResponse({"data" : dictOfAchievements})

def fill(request, current_username):
    dictOfNewAchievements = {"data" : []}
    listOfBuildings = Building.objects.all()
    listOfCheckpoints = [5,25,50,100]
    listOfRelativeXp = [25,50, 75, 150]
    listOfRelativePoints = [3,3,5,10]
    
    for building in listOfBuildings:
        print(building)
        for index, checkpoint in enumerate(listOfCheckpoints):
            challenge = "Fill up " + str(checkpoint) + " bottles in " + str(building)
            try:
                achievement = Achievement.objects.get(challenge = challenge)
            except:
                newAchievement = Achievement.objects.create(
                    name = "Lorem Ipsum",
                    challenge = challenge,
                    xp_reward = listOfRelativeXp[index],
                    points_reward = listOfRelativePoints[index]
                )
                dictOfNewAchievements["data"].append({"challenge" : challenge})

    return JsonResponse(dictOfNewAchievements)


def getAllUserAchievements(current_username):
    dictOfAchievements = []
    user = User.objects.get(username = current_username)
    
    for achievement in Achievement.objects.all():
        try:
            UserAchievement.objects.get(user = user, achievement = achievement)
            dictOfAchievements.append({"name" : achievement.name, "challenge" : achievement.challenge, "has" : True})
        except:
            dictOfAchievements.append({"name" : achievement.name, "challenge" : achievement.challenge, "has" : False})

    return dictOfAchievements


def totalFilledBottlesAchievementCheck(current_username, dictOfNewAchievements):
    user = User.objects.get(username = current_username)
    bottles = user.bottles
    listOfNewAchievements = []

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
                listOfNewAchievements.append(newUserAchievement)
            
                user.xp = user.xp + achievement.xp_reward
                user.points = user.points + achievement.points_reward
                user.save()
    
    for newAchievement in listOfNewAchievements:
        print(newAchievement.achievement.challenge)
        dictOfNewAchievements["data"].append({"name" : newAchievement.achievement.name, 
                                              "challenge" :newAchievement.achievement.challenge})

    return dictOfNewAchievements

def buildingAchievementsCheck(current_username, dictOfNewAchievements):
    user = User.objects.get(username = current_username)
    listOfNewAchievements = []

    listOfBottleCheckPoints = [5,25,50,100]
    listOfBuildingNames = Building.objects.all()

    for buildingName in listOfBuildingNames:
        building = Building.objects.get(name=buildingName)
        relevantBottles = FilledBottle.objects.filter(user=user, building=building).values()

        for bottleCheckPoints in listOfBottleCheckPoints:
            if relevantBottles.count() >= bottleCheckPoints:

                challenge = "Fill up " + str(bottleCheckPoints) + " bottles in " + str(buildingName)
                achievement = Achievement.objects.get(challenge = challenge)         
                    
                try:
                    UserAchievement.objects.get(user = user, achievement = achievement)
                except:
                    newUserAchievement = UserAchievement.objects.create(
                        user = user,
                        achievement = achievement)
                    listOfNewAchievements.append(newUserAchievement)
                
                    user.xp = user.xp + achievement.xp_reward
                    user.points = user.points + achievement.points_reward
                    user.save()
    

    for newAchievement in listOfNewAchievements:
        print(newAchievement.achievement.challenge)
        dictOfNewAchievements["data"].append({"name" : newAchievement.achievement.name, 
                                              "challenge" :newAchievement.achievement.challenge})
        
    return dictOfNewAchievements
