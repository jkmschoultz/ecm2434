'''
This module tests all functionality and validation for the achievements feature
'''

from django.test import TestCase, Client
from database.models import Achievement,UserAchievement,User,Building, FilledBottle, ShopItem, UserItem
import datetime
from django.utils import timezone
import pytz

# Create test cases for testing achievement functionality here
class TestAchievements(TestCase):
    def setUp(self):
        # Set up test case that runs before every test
        Achievement.objects.create(name="Test Name", challenge="Test challenge", xp_reward=5)
        User.objects.create(username="AchievementsTestUser",
                            email="TestUser@gmail.com",
                            name="AchievementsTestName")
        Building.objects.create(name="Test Building",
                                latitude=5,
                                longitude=5,
                                radius=1)
        Building.objects.create(name="Test Building 2",
                                latitude=10,
                                longitude=10,
                                radius=1)

    def tearDown(self):
        # Clean up run after every test method
        pass

    def testAchievementName(self):
        # Test that stringified achievement is required task for the achievement
        achievement = Achievement.objects.get(challenge="Test challenge")
        challenge = str(achievement)
        self.assertEqual(achievement.challenge, challenge)

    def testFillAchievementsEndpointEmpty(self):
        # Test that the database is filled with the correct achievements when empty
        c = Client()
        response = c.get('/achievements/fill')

        # each achievement category is tested to make sure all their related achievements are created
        self.assertTrue({"challenge" : "Fill up a bottle every day for a month"} in response.json().get("data"))
        self.assertTrue({"challenge" : "Fill up 10 bottles"} in response.json().get("data"))
        self.assertTrue({"challenge" : "Fill up 100 bottles in Test Building 2"} in response.json().get("data"))

    def testFillAchievementsEndpointFull(self):
        # Test that the database is filled with no new achievements when it has already been filled 
        # (duplicate achievements should not be created)
        c = Client()
        c.get('/achievements/fill')
        response = c.get('/achievements/fill')

        self.assertTrue(response.json() == {"data" : []})

    def testFillAchievementsEndpointPartiallyFull(self):
        # Test that the database is filled only with the achievements missing
        c = Client()
        c.get('/achievements/fill')

        # remove an achievement from each category and check that only these achievements
        # are inserted into the database
        Achievement.objects.get(challenge="Fill up 10 bottles").delete()
        Achievement.objects.get(challenge="Fill up a bottle every day for a year").delete()
        Achievement.objects.get(challenge="Fill up 5 bottles in Test Building").delete()

        response = c.get('/achievements/fill')

        # generate a list of all the new achievement names generated
        listOfNewAchievements = []
        for newAchievement in response.json().get("data"):
            listOfNewAchievements.append(newAchievement.get("challenge"))

        self.assertTrue(len(response.json().get("data")) == 3)

        self.assertTrue("Fill up 10 bottles" in listOfNewAchievements)
        self.assertTrue("Fill up a bottle every day for a year" in listOfNewAchievements)
        self.assertTrue("Fill up 5 bottles in Test Building" in listOfNewAchievements)
        
        self.assertFalse("Fill up 25 bottles in Test Building" in listOfNewAchievements)

    def testSimpleAchievement(self):
        # Test that the a user gets the correct achievements after increasing their total water bottles filled

        # sets the total bottles filled by the user to 13 so they are eligible for achievements
        user = User.objects.get(username="AchievementsTestUser")
        building = Building.objects.get(name="Test Building")
        time = datetime.datetime.now(pytz.utc)
        for day in range(13):

            # multiple bottles are filled on the same day as this should not effect these achievements
            FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=day // 3))

        # fills the achievements table so that they can be checked against the user
        c = Client()
        c.get('/achievements/fill')
        response = c.get('/achievements/check/AchievementsTestUser/')

        # generate a list of all the new achievement names generated
        listOfNewAchievements = []
        for newAchievement in response.json().get("data"):
            listOfNewAchievements.append(newAchievement.get("challenge"))

        # both of the first achievements should have been completed but the last one should not as
        # the user does not have the required number of bottles
        self.assertTrue("Fill up your first water bottle" in listOfNewAchievements)
        self.assertTrue("Fill up 10 bottles" in listOfNewAchievements)
        self.assertFalse("Fill up 25 bottles" in listOfNewAchievements)


    def testBuildingAchievementsCorrect(self):
        # Test that the user gets the correct achievements after reaching checkpoints within a building

        # have the user fill up 5 bottles in the Test Building so that they should recieve this achievement
        user = User.objects.get(username="AchievementsTestUser")
        building = Building.objects.get(name="Test Building")
        FilledBottle.objects.create(user=user, building=building, day=datetime.datetime(2023,2,12,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building, day=datetime.datetime(2023,2,17,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building, day=datetime.datetime(2023,2,25,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building, day=datetime.datetime(2023,3,4,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building, day=datetime.datetime(2023,3,7,17,5,7,tzinfo=pytz.UTC))

        # fills the achievements table so that they can be checked against the user
        c = Client()
        c.get('/achievements/fill')
        response = c.get('/achievements/check/AchievementsTestUser/')

        # generate a list of all the new achievement names generated
        listOfNewAchievements = []
        for newAchievement in response.json().get("data"):
            listOfNewAchievements.append(newAchievement.get("challenge"))

        self.assertTrue("Fill up 5 bottles in Test Building" in listOfNewAchievements)

    def testBuildingAchievementsIncorrect(self):
        # Test that the user does not get a building achievement when filling bottles in different buildings

        # have the user fill up 5 bottles in total but split between the two test buildings so
        # that they should not recieve an achievement
        user = User.objects.get(username="AchievementsTestUser")
        building = Building.objects.get(name="Test Building")
        building2 = Building.objects.get(name="Test Building 2")
        FilledBottle.objects.create(user=user, building=building, day=datetime.datetime(2023,2,12,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building2, day=datetime.datetime(2023,2,17,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building2, day=datetime.datetime(2023,2,25,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building, day=datetime.datetime(2023,3,4,17,5,7,tzinfo=pytz.UTC))
        FilledBottle.objects.create(user=user, building=building2, day=datetime.datetime(2023,3,7,17,5,7,tzinfo=pytz.UTC))

        # fills the achievements table so that they can be checked against the user
        c = Client()
        c.get('/achievements/fill')
        response = c.get('/achievements/check/AchievementsTestUser/')

        # generate a list of all the new achievement names generated
        listOfNewAchievements = []
        for newAchievement in response.json().get("data"):
            listOfNewAchievements.append(newAchievement.get("challenge"))

        self.assertFalse("Fill up 5 bottles in Test Building" in listOfNewAchievements)

    def testStreakAchievements(self):
        # Test that the user gets the correct achievement after filling up a bottle every day for a week

        # add to the FilledBottle table so that the user has filled up atleast one bottle every day for the last week, 
        # they will be filled in different locations as this should have no effect on the achievement
        user = User.objects.get(username="AchievementsTestUser")
        building = Building.objects.get(name="Test Building")
        building2 = Building.objects.get(name="Test Building 2")
        time = datetime.datetime.now(pytz.utc)
        FilledBottle.objects.create(user=user, building=building, day=time)
        FilledBottle.objects.create(user=user, building=building2, day=time - datetime.timedelta(days=1))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=2))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=3))
        FilledBottle.objects.create(user=user, building=building2, day=time - datetime.timedelta(days=4))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=5))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=6))

        # fills the achievements table so that they can be checked against the user
        c = Client()
        c.get('/achievements/fill')
        response = c.get('/achievements/check/AchievementsTestUser/')

        # generate a list of all the new achievement names generated
        listOfNewAchievements = []
        for newAchievement in response.json().get("data"):
            listOfNewAchievements.append(newAchievement.get("challenge"))

        self.assertTrue("Fill up a bottle every day for a week" in listOfNewAchievements)

    def testInvalidUsername(self):
        # Test the achievement endpoints that an invalid username simply returns an empty dictionary

        c = Client()
        response = c.get('/achievements/check/InvalidUser/')
        self.assertTrue(response.json() == {"data" : []})

        response = c.get('/achievements/InvalidUser/')
        self.assertTrue(response.json() == {"data" : []})

    def testUserXp(self):
        # Test that the user recieves the correct amount of Xp after completing an achievement

        # fill the FilledBottle table with enough bottles to give the user multiple achievements across every category
        user = User.objects.get(username="AchievementsTestUser")
        building = Building.objects.get(name="Test Building")
        time = datetime.datetime.now(pytz.utc)
        FilledBottle.objects.create(user=user, building=building, day=time)
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=1))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=2))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=3))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=4))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=5))
        FilledBottle.objects.create(user=user, building=building, day=time - datetime.timedelta(days=6))


        # give the user these achievements and the corresponding xp
        c = Client()
        c.get('/achievements/fill')
        response = c.get('/achievements/check/AchievementsTestUser/')

        # calculate how much xp the user should have recieved
        totalXpGiven = 0
        for achievement in response.json().get("data"):
            achievement = Achievement.objects.get(challenge=achievement.get("challenge"))
            totalXpGiven += achievement.xp_reward

        
        # verify that the user now has this xp
        user = User.objects.get(username="AchievementsTestUser")
        self.assertTrue(user.xp == totalXpGiven)

    def testItemRewards(self):
        # Test that a user recieves the correct item when the achievement grants one

        user = User.objects.get(username="AchievementsTestUser")
        building = Building.objects.get(name="Test Building")
        time = datetime.datetime.now(pytz.utc)

        # add item reward to the achievement for filling 1 bottle
        ShopItem.objects.create(name="Test Item",
                                type="Background",
                                cost=0,
                                availableForPurchase=False)
        
        c = Client()
        c.get('/achievements/fill')

        achievement = Achievement.objects.get(challenge="Fill up your first water bottle")
        achievement.item_reward = ShopItem.objects.get(name="Test Item")
        achievement.save()

        FilledBottle.objects.create(user=user, building=building, day=time)

        response = c.get('/achievements/check/AchievementsTestUser/')

        try:
            UserItem.objects.get(user=user, item=ShopItem.objects.get(name="Test Item"))
        except:
            self.assertTrue(False)



