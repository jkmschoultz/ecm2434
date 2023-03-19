from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

from database.models import UserFriend, User

class allFriends(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # endpoint function to return all the friends of the user making the post request

        # search the UserFriend table for all pairs of users including the specified user
        user = request.user
        friendsQuery = UserFriend.objects.filter(user=user) | UserFriend.objects.filter(friend=user)

        listOfFriends = []
        for friendsPair in friendsQuery:
            if friendsPair.user == user:
                listOfFriends.append({"username" : friendsPair.friend.username})
            else:
                listOfFriends.append({"username" : friendsPair.user.username})
        
        dictOfFriends = {"data" : listOfFriends}

        return JsonResponse(dictOfFriends)

