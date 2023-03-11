from database.models import *
from django.test import TestCase, Client
from users import views
from achievements.views import getAllUserAchievements

class TestUser(TestCase):
    def setUp(self):
        User.objects.create(username = "unitTestUS", email = "test@gmail.com", name = "unitTest",
            xp = 20, points = 7, has_been_verified = False)

    # Clean up run after every test method    
    def tearDown(self):
        pass

    # Test that /buildusersings/<username> path returns correct building information
    def testUserProfileData(self):
        c = Client()
        user = User.objects.get(username='unitTestUS')
        response = c.get('/users/' + 'unitTestUS' + '/')
        data = response.json()
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.xpLeft, data['XP'])
        self.assertEqual(user.level, data['level'])
        self.assertEqual(user.streak, data['streak'])
        self.assertEqual(user.email, data['points'])
        self.assertEqual(getAllUserAchievements('unitTestUS'), data["achievements"])

    # Test to see if the endpoint for verifing a user works
    def testUserVerifing(self):
        c = Client()
        user = User.objects.get(username='unitTestUS')
        self.assertEqual(user.has_been_verified, False)
        c.get('/users/' + 'unitTestUS' + '/verify/')
        self.assertEqual(user.has_been_verified, True)

    # Test to see if the endpoint adds 10 xp when a bottle is filled
    def testUserVerifing(self):
        c = Client()
        user = User.objects.get(username='unitTestUS')
        self.assertEqual(user.xp, 20)
        c.get('/users/' + 'unitTestUS' + '/fillBottle/')
        self.assertEqual(user.xp, 30)

    # Test to see if the endpoint for changing name works
    def testUserVerifing(self):
        c = Client()
        user = User.objects.get(username='unitTestUS')
        self.assertEqual(user.name, 'unitTest')
        c.get('/users/' + 'unitTest' + '/setName/' + 'bob/')
        self.assertEqual(user.name, 'bob')
        

    
