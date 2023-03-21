"""
This module contains the endpoints and relevant functions related to the user shop where
they may spend their points on items to customize their profile.
"""


import math
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from database.models import UserAchievement,User,Achievement, FilledBottle, Building, ShopItem, UserItem



def allAvailable(request, current_username : str) -> JsonResponse:
    # endpoint function that returns a dictionary of all the purchasable items that the specified user
    # does not own, each with a boolean value determining if the user currently has enough points to purchase the item.

    # get all items in the ShopItem table and filter out the items that the user owns and 
    dictOfUnownedItems = {"data" : []}
    user = User.objects.get(username=current_username)
    shopItems = ShopItem.objects.all()
    userItems = UserItem.objects.filter(user=user)

    listOfUserItems = []
    for userItem in userItems:
        listOfUserItems.append(userItem.item)

    for item in shopItems:
        if item not in listOfUserItems and item.availableForPurchase == True:
            
            # add this item to the dictionary with the corresponding boolean value
            if item.cost <= user.points:
                dictOfUnownedItems.get("data").append({"name" : item.name, "item type" : item.type,
                                                        "purchasable" : True, "cost" : item.cost})
            else:
                dictOfUnownedItems.get("data").append({"name" : item.name, "item type" : item.type,
                                                        "purchasable" : False, "cost" : item.cost})

    return JsonResponse(dictOfUnownedItems)

def someAvailable(request, current_username : str, item_type : str) -> JsonResponse:
    # endpoint function that returns a dictionary of all the items of the given type (i.e background, border, etc...)
    # that the specified user does not own, each woth a boolean value determining if the user 
    # currently has enough points to purchase the item.

    # get all items in the ShopItem table and filter out the items that the user owns
    dictOfUnownedItems = {"data" : []}
    user = User.objects.get(username=current_username)
    shopItems = ShopItem.objects.all()
    userItems = UserItem.objects.filter(user=user)

    listOfUserItems = []
    for userItem in userItems:
        listOfUserItems.append(userItem.item)

    for item in shopItems:
        if item not in listOfUserItems and item.type == item_type and item.availableForPurchase == True:
            
            # add this item to the dictionary with the corresponding boolean value
            if item.cost <= user.points:
                dictOfUnownedItems.get("data").append({"name" : item.name, "item type" : item.type,
                                                        "purchasable" : True, "cost" : item.cost})
            else:
                dictOfUnownedItems.get("data").append({"name" : item.name, "item type" : item.type,
                                                        "purchasable" : False, "cost" : item.cost})

    return JsonResponse(dictOfUnownedItems)

def purchase(request, current_username : str, item_name : str) -> JsonResponse:
    # endpoint function for the purchase of an item by the user. The cost of the item shoud be deducted from
    # the user's points and the item should be added to the UserItems table, the item is returned in the JsonResponse
    # to show that the purchase was successful.

    user = User.objects.get(username=current_username)
    item = ShopItem.objects.get(name=item_name)

    # check that the user does not already own the item
    try:
        UserItem.objects.get(user=user, item=item)
        return JsonResponse({"data" : ""})
    except:
        pass

    # check that the item is eligible for purchasing
    if not item.availableForPurchase:
        return JsonResponse({"data" : ""})

    # check that user has enough points to purchase the item
    if user.points >= item.cost:
        UserItem.objects.create(user=user, item=item)
        user.points = user.points - item.cost
        user.save()
        return JsonResponse({"data" : str(item)})
    else:   
        return JsonResponse({"data" : ""})

def allOwned(request, current_username : str) -> JsonResponse:
    # endpoint function that returns a dictionary all items currently owned by the specified user.

    # get all items in the UserItem table that relate to the specified user
    dictOfUnownedItems = {"data" : []}
    user = User.objects.get(username=current_username)
    userItems = UserItem.objects.filter(user=user)

    for userItem in userItems:
        dictOfUnownedItems.get("data").append(str(userItem.item))

    return JsonResponse(dictOfUnownedItems)

def someOwned(request, current_username : str, item_type : str) -> JsonResponse:
    # endpoint function that returns a dictionary of all items of a given type (i.e background, border, etc...)
    # that the specified user currently owns.
    
    # get all items in the UserItem table that relate to the specified user
    dictOfUnownedItems = {"data" : []}
    user = User.objects.get(username=current_username)
    userItems = UserItem.objects.filter(user=user)

    for userItem in userItems:

        # only add the item to the response dictionary if the item is of the right type
        if userItem.item.type == item_type:
            dictOfUnownedItems.get("data").append(str(userItem.item))

    return JsonResponse(dictOfUnownedItems)

class AuthAllAvailable(APIView):
    # Redirect to get all purchasable items for an authenticated user
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get username of authenticated user and redirect
        user = request.user
        print(request.user)
        return redirect('shop:allAvailable', current_username=user.username)
    
class AuthSomeAvailable(APIView):
    # Redirect to get purchasable items for a given type
    permission_classes = [IsAuthenticated]

    def get(self, request, item_type):
        # Get username of authenticated user and redirect
        user = request.user
        return redirect('shop:someAvailable', current_username=user.username, item_type=item_type)

class AuthPurchase(APIView):
    # Allow an authenticated user to purchase an item
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get username of authenticated user and redirect
        user = request.user
        # Get name of item being purchased from post body
        item = ''
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            item = str( body_data.get('item_name'))
        except:
            item = str( request.POST['item_name'] )

        # Redirect to purchase of item if found
        if item != '':
            return redirect('shop:purchase', current_username=user.username, item_name=item)
        else:
            return HttpResponseBadRequest('Must provide name of item to purchase')

class AuthAllOwned(APIView):
    # Get all items owned for an authenticated user
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get username of authenticated user and redirect
        user = request.user
        return redirect('shop:allOwned', current_username=user.username)

class AuthSomeOwned(APIView):
    # Get items of a specified type that are owned by an authenticated user
    permission_classes = [IsAuthenticated]

    def get(self, request, item_type):
        # Get username of authenticated user and redirect
        user = request.user
        return redirect('shop:someOwned', current_username=user.username, item_type=item_type)

