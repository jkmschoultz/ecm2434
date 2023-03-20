'''from database.models import *
from django.test import TestCase, Client
from quiz import views
import json

class TestUser(TestCase):
    def setUp(self):
        building = Building.objects.create(name='test', latitude=10, longitude=10, radius=5)

    # Clean up run after every test method    
    def tearDown(self):
        pass

    def testQuiz(self):
        quizPost = json.loads({})'''