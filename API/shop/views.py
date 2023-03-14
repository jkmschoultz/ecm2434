"""
This module contains the endpoints and relevant functions related to the user shop where
they may spend their points on items to customize their profile.
"""


import math
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database.models import UserAchievement,User,Achievement, FilledBottle, Building



def allAvailable(request, current_username : str) -> JsonResponse:
    # endpoint function that returns a dictionary of all the items that the specified user
    # does not own, each with a boolean value determining if the user currently has enough points to purchase the item.

    return JsonResponse({"data" : []})

def someAvailable(request, current_username : str, item_type : str) -> JsonResponse:
    # endpoint function that returns a dictionary of all the items of the given type (i.e background, border, etc...)
    # that the specified user does not own, each woth a boolean value determining if the user 
    # currently has enough points to purchase the item.
    
    return JsonResponse({"data" : []})

def purchase(request, current_username : str, itemID : int) -> JsonResponse:
    # endpoint function for the purchase of an item by the user. The cost of the item shoud be deducted from
    # the user's points and the item should be added to the UserItems table, the item is returned in the JsonResponse
    # to show that the purchase was successful.
    
    return JsonResponse({"data" : []})

def allOwned(request, current_username : str) -> JsonResponse:
    # endpoint function that returns a dictionary all items currently owned by the specified user.
    
    return JsonResponse({"data" : []})

def someOwned(request, current_username : str, item_type : str) -> JsonResponse:
    # endpoint function that returns a dictionary of all items of a given type (i.e background, border, etc...)
    # that the specified user currently owns.
    
    return JsonResponse({"data" : []})