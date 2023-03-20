from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

import json
from django.utils import timezone
import datetime
import pytz

from database.models import UserFriend, User, PendingFriendInvite, FilledBottle

class allFriends(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # endpoint function to return all the friends of the user making the post request

        # search the UserFriend table for all pairs of users including the specified user
        user = request.user
        friendsQuery = UserFriend.objects.filter(user=user) | UserFriend.objects.filter(friend=user)

        # add the username paired with the user's to the dictionary to be returned
        listOfFriends = []
        for friendsPair in friendsQuery:
            if friendsPair.user == user:
                listOfFriends.append({"username" : friendsPair.friend.username})
            else:
                listOfFriends.append({"username" : friendsPair.user.username})
        
        dictOfFriends = {"data" : listOfFriends}

        return JsonResponse(dictOfFriends)
    
class allPending(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # endpoint function to pending invites the user has recieved

        # search the PendingFriendInvite table for all records of the user having a pending invite sent to them
        user = request.user
        friendsQuery = PendingFriendInvite.objects.filter(potentialFriend=user)

        # add the username of the requesters to the dictionary to be returned
        listOfPendingFriends = []
        for friend in friendsQuery:
                listOfPendingFriends.append({"username" : friend.potentialFriend.username})
        
        dictOfFriends = {"data" : listOfPendingFriends}

        return JsonResponse(dictOfFriends)
    
class request(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # endpoint function to allow a user to request the friendship of another user

        user = request.user
        friend = ""
        if request.method == 'POST':
            # get the friend username from POST request
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                friend = float( body_data.get('friend username'))
            except:
                friend = float( request.POST['friend username'] )

        # validate that the friend is a real user
        try:
            friend = User.objects.get(username=friend)
        except:
            return JsonResponse({"data" : []})
        
        PendingFriendInvite.objects.create(user=user, potentialFriend=friend)
        
        return JsonResponse({"data" : {"username" : friend.username}})
    
class accept(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # endpoint function to allow a user to accept the friendship request of another user

        user = request.user
        friend = ""
        if request.method == 'POST':
            # get the friend username from POST request
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                friend = float( body_data.get('friend username'))
            except:
                friend = float( request.POST['friend username'] )

        # validate that the request is real
        try:
            friend = User.objects.get(username=friend)
            invite = PendingFriendInvite.objects.get(user=friend, potentialFriend=user)
        except:
            return JsonResponse({"data" : []})
        
        # make them friends <3
        PendingFriendInvite.objects.delete(invite)
        UserFriend(user=user, friend=friend)
        
        return JsonResponse({"data" : {"user" : user.username}, "friend" : friend.username})
    
class leaderboard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # endpoint function to return a sorted list of all the user's friends number of bottles
        # filled in the last week

        user = request.user
        friendsQuery = UserFriend.objects.filter(user=user) | UserFriend.objects.filter(friend=user)
        
        # get a list of all the user's friends
        listOfFriends = []
        for friendsPair in friendsQuery:
            if friendsPair.user == user:
                listOfFriends.append({"username" : friendsPair.friend.username})
            else:
                listOfFriends.append({"username" : friendsPair.user.username})

        # get the bottles of all the friends in the last week and sort them
        todaysDate = timezone.now()
        endDate = todaysDate - datetime.timedelta(days=7)

        listOfScores = []
        userCount = FilledBottle.objects.filter(user=user,day__range=(todaysDate, endDate)).values().count()
        listOfScores.append({"username" : user.username, "bottles" : userCount})

        for friendUsername in listOfFriends:

            # get the score for a friend
            friend = User.objects.get(username=friendUsername)
            friendCount = FilledBottle.objects.filter(user=friend,day__range=(todaysDate, endDate)).values().count()
            inserted = False

            # insert it in the right place in the list of scores
            for index, score in enumerate(listOfScores):
                if score.get("bottles") < friendCount:
                    listOfScores.insert(index, {"username" : friend.username, "bottles" : friendCount})
                    inserted = True
                    break

            if inserted == False:
                listOfScores.append({"username" : friend.username, "bottles" : friendCount})

        
        return JsonResponse({"data" : listOfScores})
    

