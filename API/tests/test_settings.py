from django.test import TestCase, Client

# Create test cases for testing django settings and basic functionality here
class TestBuildings(TestCase):
    def test_get_request(self):
        # Test that get requests to backend work
        c = Client()
        response = c.get('')
        self.assertEqual(response.status_code, 200)

    def test_response_data(self):
        # Test that reponse contains expected data
        c = Client()
        response = c.get('')
        data = response.json()
        assert(data['date'])
        assert(data['time'])
