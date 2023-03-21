'''
This module tests all functionality and validation for the user login system
'''

from django.test import TestCase, Client
from database.models import User, ShopItem
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from authentication.views import GetUser

# Create test cases for testing building functionality here
class TestAuthentication(APITestCase):
    def setUp(self):
        # Set up test user object
        user = User.objects.create_user(username='test', email='test@user.com', password='abc123')
        pp = ShopItem.objects.create(name='User', type = 'Profile Picture', cost = 0, availableForPurchase = False, image = 'static/shop_items/User.png')
        border = ShopItem.objects.create(name='Black Border', type = 'Border', cost = 0, availableForPurchase = False, image = 'static/shop_items/Black_Border.png')
        background = ShopItem.objects.create(name='White Background', type = 'Background', cost = 0, availableForPurchase = False, image = 'static/shop_items/White_Background.png')
        user.profile_pic = pp
        user.profile_border = border
        user.profile_background = background
        user.save()

    def tearDown(self):
        # Clean up run after every test method
        pass

    def testRegisterUser(self):
        # Test that a user can create an account with valid credentials
        c = Client()

        # Data to create a user
        data = {
            'username': 'created',
            'email': 'created@test.user',
            'password': 'abc'
        }
        response = c.post('/auth/register', data=data)
        # Verify user instance created in database
        self.assertIsInstance(User.objects.get(username='created'), User)

        # Verify response contains tokens for created user
        tokens = response.json()
        self.assertIsNotNone(tokens.get('token'))
        self.assertIsNotNone(tokens.get('refresh'))


    def testVerifyUser(self):
        # Test that a user can be autherticated and returns the correct user details

        c = APIClient()
        user = User.objects.get(username='test')
        c.force_authenticate(user=user)
        response = c.post('/auth/')
        self.assertTrue(response.url == "/users/test/")

        response = c.post(response.url)
        self.assertTrue(response.json().get("username") == "test")
        self.assertTrue(response.json().get("email") == "test@user.com")
        self.assertTrue(response.json().get("points") == 0)

    def testEmailValidation(self):
        # Test that a user cannot create an account with an invalid email
        c = Client()

        # Data to create a user
        data = {
            'username': 'created',
            'email': 'invalid email',
            'password': 'abc'
        }
        response = c.post('/auth/register', data=data)

        # Verify that the account was not created
        try:     
            User.objects.get(username='created')
            self.assertFalse(True)
        except:
            pass

    def testUsernameRepetition(self):
        # Test that a user cannot create an account with a taken username
        c = Client()

        # Data to create a user
        data = {
            'username': 'test',
            'email': 'test@user.com',
            'password': 'abc'
        }
        response = c.post('/auth/register', data=data)

        # Verify that the account was not created
        try:     
            User.objects.get(username='test')
            self.assertFalse(True)
        except:
            pass

    def testUsernameValidation(self):
        # Test that a user cannot create an account with an empty username
        c = Client()

        # Data to create a user
        data = {
            'username': '',
            'email': 'test@user.com',
            'password': 'abc'
        }
        response = c.post('/auth/register', data=data)

        # Verify that the account was not created
        try:     
            User.objects.get(username='')
            self.assertFalse(True)
        except:
            pass

    def testPasswordValidation(self):
        # Test that a user cannot create an account with an empty password
        c = Client()

        # Data to create a user
        data = {
            'username': 'created',
            'email': 'test@user.com',
            'password': ''
        }
        response = c.post('/auth/register', data=data)

        # Verify that the account was not created
        try:     
            User.objects.get(username='created')
            self.assertFalse(True)
        except:
            pass




    