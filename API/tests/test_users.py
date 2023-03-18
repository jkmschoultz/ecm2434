from database.models import *
from django.test import TestCase, Client
from users import views
from achievements.views import getAllUserAchievements

class TestUser(TestCase):
    def setUp(self):
        User.objects.create(username = "unitTestUser", email = "test@gmail.com", name = "unitTest",
            xp = 20, points = 7, has_been_verified=False)

    # Clean up run after every test method    
    def tearDown(self):
        pass

    # Test that /buildusersings/<username> path returns correct building information
    def testUserProfileData(self):
        c = Client()
        user = User.objects.get(username='unitTestUser')
        response = c.get('/users/unitTestUser/')
        data = response.json()
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.xpLeft, data['XP'])
        self.assertEqual(user.level, data['level'])
        self.assertEqual(user.email, data['points'])
        self.assertEqual(getAllUserAchievements('unitTestUser'), data["achievements"])

    # Test to see if the endpoint for verifing a user works
    def testUserVerifing(self):
        c = Client()
        user = User.objects.get(username='unitTestUser')
        self.assertFalse(user.has_been_verified)
        c.get('/users/unitTestUser/verify/')
        updated_user = User.objects.get(username='unitTestUser')
        self.assertTrue(updated_user.has_been_verified)

    # Test to see if the endpoint adds 10 xp when a bottle is filled
    def testUserFillBottle(self):
        c = Client()
        user = User.objects.get(username='unitTestUser')
        self.assertEqual(user.xp, 20)
        c.get('/users/' + 'unitTestUser' + '/fillBottle/')
        updated_user = User.objects.get(username='unitTestUser')
        self.assertEqual(updated_user.xp, 30)

    # Test to see if the endpoint for changing name works
    def testUserName(self):
        c = Client()
        user = User.objects.get(username='unitTestUser')
        self.assertEqual(user.name, 'unitTest')
        c.get('/users/' + 'unitTestUser' '/setName/' + 'bob' + '/')
        updated_user = User.objects.get(username='unitTestUser')
        self.assertEqual(updated_user.name, 'bob')
        

    
