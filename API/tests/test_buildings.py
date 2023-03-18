from django.test import TestCase, Client
from database.models import Building
from buildings.buildings import get_six_closest

# Create test cases for testing building functionality here
class TestBuildings(TestCase):
    def setUp(self):
        # Set up test building objects for use in test cases
        for i in range(10):
            Building.objects.create(
                name='test' + str(i),
                latitude=i * 10,
                longitude=i * 10,
                radius=5,
                image='test' + str(i)
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
