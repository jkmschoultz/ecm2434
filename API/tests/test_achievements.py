from django.test import TestCase, Client
from database.models import Achievement,UserAchievement,User,Building

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

    def tearDown(self):
        # Clean up run after every test method
        pass

    def testAchievementName(self):
        # Test that stringified achievement is required task for the achievement
        achievement = Achievement.objects.get(challenge="Test challenge")
        challenge = str(achievement)
        self.assertEqual(achievement.challenge, challenge)

    def testFillAchievementsEndpoint(self):
        # Test that the database is filled with the correct achievements when empty
        c = Client()
        response = c.get('/achievements/fill/AchievementsTestUser/')

        # each achievement category is tested to make sure all their related achievements are created
        self.assertTrue({"challenge" : "Fill up a bottle every day for a month"} in response.json().get("data"))
        self.assertTrue({"challenge" : "Fill up 10 bottles"} in response.json().get("data"))
        self.assertTrue({"challenge" : "Fill up 100 bottles in Test Building"} in response.json().get("data"))

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