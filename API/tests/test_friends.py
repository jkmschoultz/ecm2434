from django.test import TestCase, Client
from database.models import User, UserFriend, PendingFriendInvite, CustomAccountManager

from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.views import *

# Create test cases for testing friends functionality here
class TestFriends(TestCase):

    def setUp(self):
        # Set up test case that runs before every test
        User.objects.create(username="TestUser",
                            email="TestUser@gmail.com",
                            name="TestName")

    def testAllFriendsEndpoint(self):
        # Test that the AllFriends endpoint returns a list of all the friends of the user

        c = Client()
        c.login(username="TestUser", password="")
        
        # Test post request
        data = {}
        response = c.post('/friends/allFriends', data=data)
        #response = response.json().get('data')
        print(response)



