from django.test import TestCase, Client
from database.models import Building, Leaderboard, User

# Create test cases for testing building functionality here
class TestBuildings(TestCase):
    def setUp(self):
        # Set up test case that runs before every test
        building = Building.objects.create(name='test', latitude=10, longitude=10, radius=5)

        user1 = User.objects.create(username = "unitTestUS1", email = "test1@gmail.com", name = "unitTest1")
        user2 = User.objects.create(username = "unitTestUS2", email = "test2@gmail.com", name = "unitTest2")
        user3 = User.objects.create(username = "unitTestUS3", email = "test3@gmail.com", name = "unitTest3")
        user4 = User.objects.create(username = "unitTestUS4", email = "test4@gmail.com", name = "unitTest4")
        user5 = User.objects.create(username = "unitTestUS5", email = "test5@gmail.com", name = "unitTest5")

        Leaderboard.objects.create(building = building , user = user1 , user_points_in_building = 1)
        Leaderboard.objects.create(building = building , user = user1 , user_points_in_building = 2)
        Leaderboard.objects.create(building = building , user = user1 , user_points_in_building = 3)
        Leaderboard.objects.create(building = building , user = user1 , user_points_in_building = 4)
        Leaderboard.objects.create(building = building , user = user1 , user_points_in_building = 5)

    def tearDown(self):
        # Clean up run after every test method
        pass

    def test_building_name(self):
        # Test that stringified building is name of building
        building = Building.objects.get(name='test')
        name = str(building)
        self.assertEqual(building.name, name)

    def test_get_building_details(self):
        # Test that /buildings/<building_id> path returns correct building information
        c = Client()
        building = Building.objects.get(name='test')
        response = c.get('/buildings/' + str(building.id) + '/')
        data = response.json()
        self.assertEqual(building.name, data['name'])
        self.assertEqual(building.latitude, data['latitude'])
        self.assertEqual(building.longitude, data['longitude'])

    # Test to see if the endpoint for getting the top five in a building
    def testLeaderBoards(self):
        c = Client()
        building = Building.objects.get(name='test')
        response = c.get(building.id + '/leaderboard/')
        data = response.json()
        self.assertEqual(5, len(data['names']))
        self.assertEqual(5, len(data['points']))
        self.assertEqual(4, data['points'][3])
        self.assertEqual(5, data['points'][4])
        self.assertEqual('unitTest4', data['names'][3])
        self.assertEqual('unitTest5', data['names'][4])
