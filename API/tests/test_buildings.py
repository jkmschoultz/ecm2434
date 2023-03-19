from django.test import TestCase, Client
from database.models import Building, Leaderboard, User
from buildings.buildings import get_six_closest

# Create test cases for testing building functionality here
class TestBuildings(TestCase):
    def setUp(self):
        # Set up test objects for use in each of the test cases
        for i in range(10):
            Building.objects.create(
                name='test' + str(i),
                latitude=i * 10,
                longitude=i * 10,
                radius=5,
                image='test' + str(i)
            )

        building = Building.objects.create(name='test', latitude=10, longitude=10, radius=5)

        user1 = User.objects.create(username = "unitTestUS1", email = "test1@gmail.com", name = "unitTest1")
        user2 = User.objects.create(username = "unitTestUS2", email = "test2@gmail.com", name = "unitTest2")
        user3 = User.objects.create(username = "unitTestUS3", email = "test3@gmail.com", name = "unitTest3")
        user4 = User.objects.create(username = "unitTestUS4", email = "test4@gmail.com", name = "unitTest4")
        user5 = User.objects.create(username = "unitTestUS5", email = "test5@gmail.com", name = "unitTest5")

        Leaderboard.objects.create(building = building , user = user1 , user_points_in_building = 1)
        Leaderboard.objects.create(building = building , user = user2 , user_points_in_building = 2)
        Leaderboard.objects.create(building = building , user = user3 , user_points_in_building = 3)
        Leaderboard.objects.create(building = building , user = user4 , user_points_in_building = 4)
        Leaderboard.objects.create(building = building , user = user5 , user_points_in_building = 5)

    def tearDown(self):
        # Clean up run after every test method
        pass

    def test_created_building(self):
        # Test that test building created properly
        building = Building.objects.get(name='test1')

        # Assert building contains correct values
        self.assertEqual(building.latitude, 10)
        self.assertEqual(building.longitude, 10)
        self.assertEqual(building.radius, 5)

        # Check stringified building is name of building
        name = str(building)
        self.assertEqual(building.name, name)

    def test_get_six_closest(self):
        # Test getting 6 buildings closest to a position
        buildings = get_six_closest(0, 0)
        self.assertEqual(len(buildings), 6)
        # Assert 5 closest buildings are correctly ordered
        for i in range(5):
            name = buildings[i]['name']
            expected = 'test' + str(i)
            self.assertEqual(name, expected)
    
    def test_is_accessible(self):
        # Test building accessibility
        buildings = get_six_closest(8, 8)
        # Assert first building is accessible
        self.assertEqual(buildings[0]['name'], 'test1')
        self.assertTrue(buildings[0]['is_accessible'])
        for building in buildings[1:]:
            # Assert remaining buildings are not accessible
            self.assertFalse(building['is_accessible'])
    
    def test_not_accessible(self):
        # Test that buildings should not be accessible
        buildings = get_six_closest(-5, -5)
        for building in buildings:
            self.assertFalse(building['is_accessible'])

    def test_get_building_details(self):
        # Test that /buildings/<building_id> path returns correct building information
        c = Client()
        # Simulate get request
        building = Building.objects.get(name='test1')
        response = c.get('/buildings/' + str(building.id) + '/')
        data = response.json()
        # Verify response is same as expected building
        self.assertEqual(building.name, data['name'])
        self.assertEqual(building.latitude, data['latitude'])
        self.assertEqual(building.longitude, data['longitude'])

    def test_fail_get_building(self):
        # Test getting a building that does not exist
        c = Client()
        # Simulate get request
        response = c.get('/buildings/-1/')
        # Assert response code is 404 not found
        self.assertEqual(response.status_code, 404)

    def testLeaderBoards(self):
        # Test to see if the endpoint for getting the top five in a building
        c = Client()
        building = Building.objects.get(name='test')
        response = c.get('/buildings/' + str(building.name) + '/leaderboard/')
        data = response.json()
        self.assertEqual(5, len(data['names']))
        self.assertEqual(5, len(data['points']))
        self.assertEqual(4, data['points'][3])
        self.assertEqual(5, data['points'][4])
        self.assertEqual('unitTest4', data['names'][3])
        self.assertEqual('unitTest5', data['names'][4])
