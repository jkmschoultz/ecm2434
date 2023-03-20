from django.test import TestCase, Client
from database.models import User, UserFriend, PendingFriendInvite, CustomAccountManager

from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework_simplejwt.views import *

# Create test cases for testing friends functionality here
class TestFriends(TestCase):

    def setUp(self):
        # Set up test case that runs before every test
        User.objects.create_user(username="TestUser", email="test@gmail.com", password="test")

    def testAllFriendsEndpoint(self):
        # Test that the AllFriends endpoint returns a list of all the friends of the user

        user = User.objects.get(username='TestUser')

        # create 3 users but only add 2 of them as friends
        User.objects.create(username="TestFriend1",
                    email="TestFriend1@gmail.com",
                    name="TestName")
        User.objects.create(username="TestFriend2",
            email="TestFriend2@gmail.com",
            name="TestName")
        User.objects.create(username="TestFriend3",
            email="TestFriend3@gmail.com",
            name="TestName")
        
        UserFriend.objects.create(user=user, friend=User.objects.get(username="TestFriend1"))
        UserFriend.objects.create(user=user, friend=User.objects.get(username="TestFriend2"))

        c = APIClient()
        c.force_authenticate(user=user)
        
        # Test post request to get all of the user's friends
        data = {}
        response = c.post('/friends/allFriends', data=data)
        
        self.assertTrue(len(response.json().get("data")) == 2)
        self.assertTrue({"username" : "TestFriend1"} in response.json().get("data"))



