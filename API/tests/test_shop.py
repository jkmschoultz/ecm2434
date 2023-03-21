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
        unaffordableItem = {"name":"Test Item 1", "item type" : "Border", "purchasable" : False, "cost" : 25}
        affordableItem = {"name":"Test Item 2", "item type" : "Border", "purchasable" : False, "cost" : 15}
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
        item = {"name":"Test Item 2", "item type" : "Border", "purchasable" : False, "cost" : 15}
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
        item1 = {"name":"Test Item 1", "item type" : "Border", "purchasable" : False, "cost" : 25}
        item2 = {"name":"Test Item 2", "item type" : "Border", "purchasable" : True, "cost" : 15}
        item3 = {"name":"Test Item 3", "item type" : "Background", "purchasable" : False, "cost" : 25}
        item4 = {"name":"Test Item 4", "item type" : "Background", "purchasable" : True, "cost" : 20}

        self.assertTrue(item1 in response.json().get("data"))
        self.assertTrue(item2 in response.json().get("data"))
        self.assertTrue(item3 in response.json().get("data"))
        self.assertTrue(item4 in response.json().get("data"))

    def testPurchaseEndpointWhenValid(self):
        # Test that a user with enough points can purchase an item

        # set the user points to 20 so the item is affordable
        user = User.objects.get(username="TestUser")
        user.points = 20
        user.save()

        c = Client()
        response = c.get('/shop/purchase/TestUser/Test%20Item%202')

        # the cost of the item should be deducted from the user and the item should be returned in the response,
        # there should also be a record of the item in the UserItems
        user = User.objects.get(username="TestUser")
        item = ShopItem.objects.get(name="Test Item 2")
        self.assertTrue(user.points == 20 - item.cost)
        self.assertTrue(response.json().get("data") == str(item))

        try:
            UserItem.objects.get(user=user, item=item)
        except:
            self.assertFalse(True)

    def testPurchaseEndpointWhenInvalid(self):
        # Test that a user with insufficient points can't purchase an item

        # set the user points to 10 so it can be tested that the points are unchanged
        user = User.objects.get(username="TestUser")
        user.points = 10
        user.save()

        c = Client()
        response = c.get('/shop/purchase/TestUser/Test%20Item%202')

        # the purchase should be unsuccessful and the response should be empty
        user = User.objects.get(username="TestUser")
        item = ShopItem.objects.get(name="Test Item 2")
        self.assertTrue(user.points == 10)
        self.assertTrue(response.json().get("data") == "")

        # there should not be a record of the user owning the item
        try:
            UserItem.objects.get(user=user, item=item)
            self.assertFalse(True)
        except:
            pass

    def testPurchaseEndpointWhenOwned(self):
        # Test that the user cannot purchase an item that they already own

        # set the user points to 100 so they have enough points to buy an item twice
        user = User.objects.get(username="TestUser")
        user.points = 100
        user.save()

        # attempt to purchase Test Item 3 twice
        c = Client()
        c.get('/shop/purchase/TestUser/Test%20Item%203')
        response = c.get('/shop/purchase/TestUser/Test%20Item%203')

        # the cost of the item should be deducted from the user only once and the response should be empty,
        # there should only be one record of purchase in the UserItem table
        user = User.objects.get(username="TestUser")
        item = ShopItem.objects.get(name="Test Item 3")
        self.assertTrue(user.points == 100 - item.cost)
        self.assertTrue(response.json().get("data") == "")

        userItemRecords = UserItem.objects.filter(user=user, item=item)
        self.assertTrue(userItemRecords.count() == 1)


    def testAllOwned(self):
        # Test that the allOwned endpoint returns all items that the user owns

        user = User.objects.get(username="TestUser")

        UserItem.objects.create(user=user, item=ShopItem.objects.get(name="Test Item 2"))
        UserItem.objects.create(user=user, item=ShopItem.objects.get(name="Test Item 3"))

        c = Client()
        response = c.get('/shop/owned/TestUser/')

        # test that the user owns a total of 2 items
        self.assertTrue(len(response.json().get("data")) == 2)

    def testSomeOwned(self):
        # Test that the someOwned endpoint returns all items that the user owns of a specific type

        user = User.objects.get(username="TestUser")

        UserItem.objects.create(user=user, item=ShopItem.objects.get(name="Test Item 2"))
        UserItem.objects.create(user=user, item=ShopItem.objects.get(name="Test Item 3"))

        c = Client()
        response = c.get('/shop/owned/TestUser/Border/')

        # test that the response only contains 1 item as the user only has 1 item of type "Border"
        self.assertTrue(len(response.json().get("data")) == 1)




    


