'''
This module tests all functionality and validation for the user's points shop.
'''

from django.test import TestCase, Client
from database.models import Achievement,UserAchievement,User,Building, FilledBottle

# Create test cases for testing shop functionality here
class TestShop(TestCase):
    def setUp(self):
        # Set up test case that runs before every test
        User.objects.create(username="TestUser",
                            email="TestUser@gmail.com",
                            name="TestName")

    def tearDown(self):
        # Clean up run after every test method
        pass

    def testItemName(self):
        # Test that stringified items are the name of the item
        pass

    def testAllAvailableEndpoint(self):
        # Test that the allAvailable shop endpoint returns a dictionary of every item not owned by the user

        pass

    def testPurachasableBoolean(self):
        # Test that the boolean ,returned with each item when the allAvailable endpoint is called, is correct

        pass