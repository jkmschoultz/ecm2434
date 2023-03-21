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
        User.objects.create_user(username='test', email='test@user.com', password='abc123')
        pp = ShopItem.objects.create(name='User', type = 'Profile Picture', cost = 0, availableForPurchase = False, image = 'static/shop_items/User.png')
        border = ShopItem.objects.create(name='Black Border', type = 'Border', cost = 0, availableForPurchase = False, image = 'static/shop_items/Black_Border.png')
        background = ShopItem.objects.create(name='White Background', type = 'Background', cost = 0, availableForPurchase = False, image = 'static/shop_items/White_Background.png')


    def tearDown(self):
        # Clean up run after every test method
        pass

    def test_register_user(self):
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


    def test_verify_user(self):
        c = APIClient()
        user = User.objects.get(username='test')
        c.force_authenticate(user=user)
        # success = c.login(username='test', password='abc123')
        # print(success)
        response = c.post('/auth/')
        print(response)