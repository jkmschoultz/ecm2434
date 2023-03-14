'''
This module tests all functionality and validation for the user's points shop.
'''

from django.test import TestCase, Client
from database.models import Achievement,UserAchievement,User,Building, FilledBottle, ShopItem, UserItem

# Create test cases for testing shop functionality here
class TestShop(TestCase):
    def setUp(self):
        # Set up test case that runs before every test
        User.objects.create(username="TestUser",
                            email="TestUser@gmail.com",
                            name="TestName")
        ShopItem.objects.create(name="Test Item 1",
                                type="Border",
                                cost=25)
        ShopItem.objects.create(name="Test Item 2",
                                type="Border",
                                cost=15)
        ShopItem.objects.create(name="Test Item 3",
                                type="Background",
                                cost=25)

    def tearDown(self):
        # Clean up run after every test method
        pass

    def testItemName(self):
        # Test that stringified items are the name of the item and the type of item
        item = ShopItem.objects.get(name="Test Item 2")
        self.assertTrue(str(item) == "Test Item 2, Border")

    def testAllAvailableEndpoint(self):
        # Test that the allAvailable shop endpoint returns a dictionary of every item not owned by the user

        # have the user own one item already so it shouldn't be included in the response
        user = User.objects.get(username="TestUser")
        item = ShopItem.objects.get(name="Test Item 3")
        UserItem.objects.create(user=user, item=item)

        c = Client()
        response = c.get('/shop/available/TestUser/')

        # only two items should be available
        self.assertTrue(len(response.json().get("data")) == 2)
        unaffordableItem = {"name":"Test Item 1", "item type" : "Border", "purchasable" : False}
        affordableItem = {"name":"Test Item 2", "item type" : "Border", "purchasable" : False}
        self.assertTrue(affordableItem in response.json().get("data"))
        self.assertTrue(unaffordableItem in response.json().get("data"))

    def testSomeAvailableEndpoint(self):
        # Test that the someAvailable shop endpoint returns a dictionary of every item not owned by the user of 
        # a specified type

        # have the user own one item already so it shouldn't be included in the response
        user = User.objects.get(username="TestUser")
        item = ShopItem.objects.get(name="Test Item 1")
        UserItem.objects.create(user=user, item=item)

        c = Client()
        response = c.get('/shop/available/TestUser/Border/')

        # only one item is of type Border and not already owned by the user
        item = {"name":"Test Item 2", "item type" : "Border", "purchasable" : False}
        self.assertTrue(response.json().get("data") == [item])

    def testPurchasableBoolean(self):
        # Test that the purchasable boolean in the dictionary, returned by the allAvailable endpoint,
        # correcty determines if a user owns enough points to purchase the item.

        # set the user points to 20 so only some items are affordable
        user = User.objects.get(username="TestUser")
        user.points = 20
        user.save()

        # add a border case
        ShopItem.objects.create(name="Test Item 4",
                                type="Background",
                                cost=20)
        
        c = Client()
        response = c.get('/shop/available/TestUser/')

        # only two of the created items should be affordable for the user
        item1 = {"name":"Test Item 1", "item type" : "Border", "purchasable" : False}
        item2 = {"name":"Test Item 2", "item type" : "Border", "purchasable" : True}
        item3 = {"name":"Test Item 3", "item type" : "Background", "purchasable" : False}
        item4 = {"name":"Test Item 4", "item type" : "Background", "purchasable" : True}

        self.assertTrue(item1 in response.json().get("data"))
        self.assertTrue(item2 in response.json().get("data"))
        self.assertTrue(item3 in response.json().get("data"))
        self.assertTrue(item4 in response.json().get("data"))