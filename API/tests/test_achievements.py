'''
This module tests all functionality and validation for the achievements feature
'''

from django.test import TestCase, Client
from database.models import Achievement,UserAchievement,User,Building, FilledBottle
import datetime
from django.utils import timezone
import pytz

# Create test cases for testing achievement functionality here
class TestAchievements(TestCase):
    def setUp(self):
        # Set up test case that runs before every test
        Achievement.objects.create(name="Test Name", challenge="Test challenge", xp_reward=5, points_reward=3)
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
        response = c.get('/achievements/fill/AchievementsTestUser/')

        # each achievement category is tested to make sure all their related achievements are created
        self.assertTrue({"challenge" : "Fill up a bottle every day for a month"} in response.json().get("data"))
        self.assertTrue({"challenge" : "Fill up 10 bottles"} in response.json().get("data"))
        self.assertTrue({"challenge" : "Fill up 100 bottles in Test Building 2"} in response.json().get("data"))

    def testFillAchievementsEndpointFull(self):
        # Test that the database is filled with no new achievements when it has already been filled 
        # (duplicate achievements should not be created)
        c = Client()
        c.get('/achievements/fill/AchievementsTestUser/')
        response = c.get('/achievements/fill/AchievementsTestUser/')

        self.assertTrue(response.json() == {"data" : []})

    def testFillAchievementsEndpointPartiallyFull(self):
        # Test that the database is filled only with the achievements missing
        c = Client()
        c.get('/achievements/fill/AchievementsTestUser/')

        # remove an achievement from each category and check that only these achievements
        # are inserted into the database
        Achievement.objects.get(challenge="Fill up 10 bottles").delete()
        Achievement.objects.get(challenge="Fill up a bottle every day for a year").delete()
        Achievement.objects.get(challenge="Fill up 5 bottles in Test Building").delete()

        response = c.get('/achievements/fill/AchievementsTestUser/')

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

        # sets the total bottles filled by the user to 67 so they are eligible for achievements
        user = User.objects.get(username="AchievementsTestUser")
        user.bottles = 67
        user.save()

        # fills the achievements table so that they can be checked against the user
        c = Client()
        c.get('/achievements/fill/AchievementsTestUser/')
        response = c.get('/achievements/check/AchievementsTestUser/')

        # generate a list of all the new achievement names generated
        listOfNewAchievements = []
        for newAchievement in response.json().get("data"):
            listOfNewAchievements.append(newAchievement.get("challenge"))

        # both of the first achievements should have been completed but the last one should not as
        # the user does not have the required number of bottles
        self.assertTrue("Fill up your first water bottle" in listOfNewAchievements)
        self.assertTrue("Fill up 50 bottles" in listOfNewAchievements)
        self.assertFalse("Fill up 100 bottles" in listOfNewAchievements)


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
        c.get('/achievements/fill/AchievementsTestUser/')
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
        c.get('/achievements/fill/AchievementsTestUser/')
        response = c.get('/achievements/check/AchievementsTestUser/')

        # generate a list of all the new achievement names generated
        listOfNewAchievements = []
        for newAchievement in response.json().get("data"):
            listOfNewAchievements.append(newAchievement.get("challenge"))

        self.assertTrue(len(listOfNewAchievements) == 0)