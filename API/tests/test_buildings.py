from django.test import TestCase, Client
from database.models import Building, Leaderboard, User, BuildingFloor

# Create test cases for testing building functionality here
class TestBuildings(TestCase):
    def setUp(self):
        # Set up test objects for use in each of the test cases
        for i in range(10):
            building = Building.objects.create(
                name='test' + str(i),
                latitude=i * 10,
                longitude=i * 10,
                radius=5,
                image='test' + str(i)
            )
            BuildingFloor.objects.create(
                building = building,
                image = 'static/floors/Laver_6th.png',
                floorNumber = 6
            )
            BuildingFloor.objects.create(
                building = building,
                image = 'static/floors/Laver_7th.png',
                floorNumber = 7
            )

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

    def test_get_buildings(self):
        # Test getting 6 buildings closest to a position
        c = Client()

        # Test post request with position data
        data = {
            'lat': 0,
            'long': 0
        }
        response = c.post('/buildings/', data=data)
        buildings = response.json().get('data')

        # Assert returns 6 total buildings
        self.assertEqual(len(buildings), 6)
        # Assert buildings are ordered as expected
        for i in range(6):
            name = buildings[i]['name']
            expected = 'test' + str(i)
            self.assertEqual(name, expected)
        # Assert floor plans are passed with
        buildings = list(buildings)
        building_data = buildings[0]
        self.assertEqual(len(building_data['floors']),2)
    
    def test_is_accessible(self):
        # Test building accessibility
        c = Client()

        # Make post request with position that would access building
        data = {
            'lat': 8,
            'long': 8
        }
        response = c.post('/buildings/', data=data)
        buildings = response.json().get('data')

        # Assert first building is accessible and expected
        self.assertEqual(buildings[0]['name'], 'test1')
        self.assertTrue(buildings[0]['is_accessible'])
        for building in buildings[1:]:
            # Assert remaining buildings are not accessible
            self.assertFalse(building['is_accessible'])
    
    def test_not_accessible(self):
        # Test that buildings should not be accessible
        c = Client()

        # Make post request from position not in building
        data = {
            'lat': -5,
            'long': -5
        }
        response = c.post('/buildings/', data=data)
        buildings = response.json().get('data')

        # Assert none of the buildings are accessible
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
