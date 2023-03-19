from database.models import *
from django.test import TestCase, Client
import json

class TestUser(TestCase):
    def setUp(self):
        building1 = Building.objects.create(name='test', latitude=10, longitude=10, radius=5)
        user1 = User.object.create(self, username = "unitTestUser", email = "test@gmail.com", password="jibba jabba", name = "unitTest",
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
        c = Client()
        u = User.objects.get(username='unitTestUser')
        u.set_password('new password')
        u.save()
        building_test = Building.objects.get(name = 'test')
        leaderboard = Leaderboard.objects.filter(building = building_test)
        self.assertEqual(len(leaderboard), 1)
        data = {"correct": 3, "password": 'test'}
##        data.encode('utf-8')
        c.login(username='unitTestUser', password='jibba jabba')
        c.post("/quiz/", data=data)
        leaderboard_new = list(Leaderboard.objects.filter(building = building_test))
        print(leaderboard_new)
        self.assertEqual(len(leaderboard_new), 2)
        