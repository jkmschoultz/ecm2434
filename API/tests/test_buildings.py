from django.test import TestCase, Client
from database.models import Building

# Create test cases for testing building functionality here
class TestBuildings(TestCase):
    def setUp(self):
        # Set up test case that runs before every test
        Building.objects.create(name='test', latitude=10, longitude=10, radius=5)

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
