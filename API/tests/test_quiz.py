from database.models import *
from django.test import TestCase, Client
from rest_framework.test import APIClient
import json

class TestQuiz(TestCase):
    def setUp(self):
        building1 = Building.objects.create(name='test', latitude=10, longitude=10, radius=5)
        user1 = User.objects.create(username = "unitTestUser", email = "test@gmail.com", password="jibba jabba", name = "unitTest",
            xp = 20, points = 7, has_been_verified=False)
        Leaderboard.objects.create(building = building1, user = user1)

    # Clean up run after every test method    
    def tearDown(self):
        pass

    def normalize_email(self,email):
        return email
    
    def model(self,email, username, **other_fields):
        return User.objects.create(email=email, username=username, **other_fields)

    def testQuiz(self):
        building_test = Building.objects.get(name = 'test')
        leaderboard = Leaderboard.objects.filter(building = building_test)
        self.assertEqual(len(leaderboard), 1)

        user = User.objects.get(username='unitTestUser')
        c = APIClient()
        c.force_authenticate(user=user)
        
        # test post request to get all of the user's pending requests
        data = json.dumps({'correct':3,'building': 'test'})
        c.post("/quiz/", data=data)
        leaderboard = Leaderboard.objects.filter(building = building_test)
        self.assertEqual(len(leaderboard), 2)
        