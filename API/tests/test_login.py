'''
This module tests all functionality and validation for the user login system
'''

from django.test import TestCase, Client
from database.models import User

# Create test cases for testing achievement functionality here
class TestLogin(TestCase):
    def setUp(self):
        # Set up test case that runs before every test
        pass

    def tearDown(self):
        # Clean up run after every test method
        pass