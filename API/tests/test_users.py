from database.models import *
from django.test import TestCase, Client
from users import views
from achievements.views import getAllUserAchievements
from django.conf import settings

class TestUser(TestCase):
    def setUp(self):
        user = User.objects.create(username = "unitTestUser", email = "test@gmail.com", name = "unitTest",
            xp = 20, points = 7, has_been_verified=False)
        Building.objects.create(name="Test Building",
                        latitude=5,
                        longitude=5,
                        radius=1)
        pp = ShopItem.objects.create(name='User', type = 'Profile Picture', cost = 0, availableForPurchase = False, image = 'static/shop_items/User.png')
        border = ShopItem.objects.create(name='Black Border', type = 'Border', cost = 0, availableForPurchase = False, image = 'static/shop_items/Black_Border.png')
        background = ShopItem.objects.create(name='White Background', type = 'Background', cost = 0, availableForPurchase = False, image = 'static/shop_items/White_Background.png')
        user.profile_pic = pp
        user.profile_border = border
        user.profile_background = background
        user.save()

    # Clean up run after every test method    
    def tearDown(self):
        pass

    # Test that /users/<username> path returns correct building information
    def testUserProfileData(self):
        c = Client()
        user = User.objects.get(username='unitTestUser')
        response = c.get('/users/unitTestUser/')
        data = response.json()
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.xpLeft, data['XP'])
        self.assertEqual(user.level, data['level'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.points, data['points'])
        self.assertEqual(settings.BASE_URL + user.profile_pic.image.url, data['profile_pic'])
        self.assertEqual(settings.BASE_URL + user.profile_border.image.url, data['profile_border'])
        self.assertEqual(settings.BASE_URL + user.profile_background.image.url, data['profile_background'])
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
        c.get('/users/' + 'unitTestUser/' + 'Test Building' + '/fillBottle/')
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
        

    
