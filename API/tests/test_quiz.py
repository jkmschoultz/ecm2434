from database.models import *
from django.test import TestCase, Client
from rest_framework.test import APIClient
import json

class TestQuiz(TestCase):
    def setUp(self):
        building = Building.objects.create(name='test', latitude=10, longitude=10, radius=5)
        user = User.objects.create(username = "unitTestUser", email = "test@gmail.com", password="jibba jabba", name = "unitTest",
            xp = 20, points = 7, has_been_verified=False)
        Leaderboard.objects.create(building = building, user = user)

    # Clean up run after every test method    
    def tearDown(self):
        pass

    def testQuiz(self):
        # Test that user answers to quiz are correctly processed
        building_test = Building.objects.get(name = 'test')
        # Verify leaderboard exists in building
        leaderboard = Leaderboard.objects.filter(building = building_test)
        self.assertEqual(len(leaderboard), 1)

        # Simulate user answers to quiz
        user = User.objects.get(username='unitTestUser')
        c = APIClient()
        c.force_authenticate(user=user)
        data = {'correct':3,'building': 'test'}  # Sample quiz result data
        c.post("/quiz/", data=data)

        # Verify leaderboard has been updated
        leaderboard = Leaderboard.objects.filter(building = building_test)
        self.assertEqual(len(leaderboard), 1)
        entry = leaderboard[0]
        self.assertEqual(entry.user_points_in_building, 15)  # 15 points for 3 right answers
        