"""
This module contains the endpoints and relevant functions related to the user achievements feature.
"""


import math
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database.models import UserAchievement,User,Achievement, FilledBottle, Building



def detail(request, current_username) -> JsonResponse:
    # endpoint function to check if a specified user has completed any achievements they don't currently have,
    # this will be called every time a user fills a bottle.

    dictOfNewAchievements = {"data" : []}
    dictOfNewAchievements = totalFilledBottlesAchievementCheck(current_username, dictOfNewAchievements)
    dictOfNewAchievements = buildingAchievementsCheck(current_username, dictOfNewAchievements)
    # return a dictionary of any new achievements acquired so they can be displayed on the front-end
    return JsonResponse(dictOfNewAchievements)

def all(request, current_username : str) -> JsonResponse:
    # endpoint function to return a dictionary of all achievements with a boolean value
    #   to show if the user has completed this achievement.

    dictOfAchievements = getAllUserAchievements(current_username)
    return JsonResponse({"data" : dictOfAchievements})

def fill(request, current_username : str) -> JsonResponse:
    # endpoint function to create achievements relating to the amount of bottles filled in each building,
    # duplicate functions won't be created so this function should be called whenever a new building is introduced to the database.
    # will return a dictionary of new achievements that are made, an empty dictionary if none are made.

    dictOfNewAchievements = {"data" : []}
    listOfBuildings = Building.objects.all()
    listOfCheckpoints = [5,25,50,100]

    # the xp and points each achievement should have,
    # the index of the xp & points will align with the index in the list of checkpoints.
    listOfRelativeXp = [25,50, 75, 150]
    listOfRelativePoints = [3,3,5,10]

    for building in listOfBuildings:
        for index, checkpoint in enumerate(listOfCheckpoints):
            challenge = "Fill up " + str(checkpoint) + " bottles in " + str(building)

            # if the achievement does not currently exist, it will be created and added to the database.
            try:
                achievement = Achievement.objects.get(challenge = challenge)
            except:
                # IMPORTANT - the achievement is created with the name "Lorem Ipsum" as a placeholder,
                # an admin will need to change this to a proper name after the achievement is made.
                newAchievement = Achievement.objects.create(
                    name = "Lorem Ipsum",
                    challenge = challenge,
                    xp_reward = listOfRelativeXp[index],
                    points_reward = listOfRelativePoints[index]
                )
                dictOfNewAchievements["data"].append({"challenge" : challenge})

    return JsonResponse(dictOfNewAchievements)


def getAllUserAchievements(current_username : str) -> list:
    # this function returns a list of dictionaries, each dictionary is an achievement in the database and a boolean
    # representing whether the specified user has accomplished this achievement.

    listOfAchievements = []
    user = User.objects.get(username = current_username)
    
    # iterates through all achievements and checks if the user owns this achievement.
    for achievement in Achievement.objects.all():
        try:
            UserAchievement.objects.get(user = user, achievement = achievement)
            listOfAchievements.append({"name" : achievement.name, "challenge" : achievement.challenge, "has" : True})
        except:
            listOfAchievements.append({"name" : achievement.name, "challenge" : achievement.challenge, "has" : False})

    return listOfAchievements


def totalFilledBottlesAchievementCheck(current_username : str, dictOfNewAchievements : dict) -> list:
    # this function checks if a user has completed any of the total bottle achievements,
    # acquired by the user's total bottles filled surpassing one of the listed checkpoints.
    # a list of any new achievements completed is then returned.

    user = User.objects.get(username = current_username)
    bottles = user.bottles
    listOfNewAchievements = []

    listOfBottleCheckpoints = [1,5,10,50,100,250,500,1000]

    for checkpoint in listOfBottleCheckpoints:
        # if the user has filled more bottles than this checkpoint they should have this achievement
        if bottles >= checkpoint:
            if checkpoint == 1:
                challenge = "Fill up your first water bottle"
            else:
                challenge = "Fill up " + str(checkpoint) + " bottles"

            # gets the ahcievement relating to the checkpoint from the Achievements table
            achievement = Achievement.objects.get(challenge = challenge)

            # if the user does not already own this achievement it is added the UserAchievement table
            try:
                UserAchievement.objects.get(user = user, achievement = achievement)
            except:
                newUserAchievement = UserAchievement.objects.create(
                    user = user,
                    achievement = achievement)
                listOfNewAchievements.append(newUserAchievement)
            
                # give the user the rewards that accomplishing the achievement gives 
                user.xp = user.xp + achievement.xp_reward
                user.points = user.points + achievement.points_reward
                user.save()
    
    # add these new achievements to the dictionary of all the new achievements that will be returned to the front-end.
    for newAchievement in listOfNewAchievements:
        print(newAchievement.achievement.challenge)
        dictOfNewAchievements["data"].append({"name" : newAchievement.achievement.name, 
                                              "challenge" :newAchievement.achievement.challenge})

    return dictOfNewAchievements

def buildingAchievementsCheck(current_username : str, dictOfNewAchievements : dict) -> list:
    # this function checks if the user has completed any achievements relating to the total bottles filled
    # in each building.
    # a list of any new achievements completed is then returned.

    user = User.objects.get(username = current_username)
    listOfNewAchievements = []

    listOfBottleCheckPoints = [5,25,50,100]
    listOfBuildingNames = Building.objects.all()

    for buildingName in listOfBuildingNames:
        building = Building.objects.get(name=buildingName)

        # queries the FilledBottle table to get all the bottles filled by the specified user in the specified building
        relevantBottles = FilledBottle.objects.filter(user=user, building=building).values()

        for bottleCheckPoints in listOfBottleCheckPoints:
            # if the user has filled more bottles in the building than this checkpoint they should have this achievement
            if relevantBottles.count() >= bottleCheckPoints:

                challenge = "Fill up " + str(bottleCheckPoints) + " bottles in " + str(buildingName)
                achievement = Achievement.objects.get(challenge = challenge)         
                    
                # if the user does not already own this achievement it is added the UserAchievement table
                try:
                    UserAchievement.objects.get(user = user, achievement = achievement)
                except:
                    newUserAchievement = UserAchievement.objects.create(
                        user = user,
                        achievement = achievement)
                    listOfNewAchievements.append(newUserAchievement)
                
                    # give the user the rewards that accomplishing the achievement gives 
                    user.xp = user.xp + achievement.xp_reward
                    user.points = user.points + achievement.points_reward
                    user.save()
    

    # add these new achievements to the dictionary of all the new achievements that will be returned to the front-end.
    for newAchievement in listOfNewAchievements:
        print(newAchievement.achievement.challenge)
        dictOfNewAchievements["data"].append({"name" : newAchievement.achievement.name, 
                                              "challenge" :newAchievement.achievement.challenge})
        
    return dictOfNewAchievements
