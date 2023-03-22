from django.test import TestCase, Client
from database.models import Building, User, Leaderboard, ShopItem

# Create test cases for testing leaderboard functionality here
class TestLeaderboard(TestCase):
    def setUp(self):
        # Set up test objects for use in test cases
        building = Building.objects.create(name='test', latitude=10, longitude=10, radius=5)
        Building.objects.create(name='empty', latitude=0, longitude=0, radius=1)

        user = User.objects.create(username = "unitTestUS", email = "test@gmail.com", name = "unitTest")
        user1 = User.objects.create(username = "unitTestUS1", email = "test1@gmail.com", name = "unitTest1")
        user2 = User.objects.create(username = "unitTestUS2", email = "test2@gmail.com", name = "unitTest2")
        user3 = User.objects.create(username = "unitTestUS3", email = "test3@gmail.com", name = "unitTest3")
        user4 = User.objects.create(username = "unitTestUS4", email = "test4@gmail.com", name = "unitTest4")
        user5 = User.objects.create(username = "unitTestUS5", email = "test5@gmail.com", name = "unitTest5")
        user6 = User.objects.create(username = "unitTestUS6", email = "test6@gmail.com", name = "unitTest6")

        Leaderboard.objects.create(building = building , user = user , user_points_in_building = 0)
        Leaderboard.objects.create(building = building , user = user1 , user_points_in_building = 1)
        Leaderboard.objects.create(building = building , user = user2 , user_points_in_building = 2)
        Leaderboard.objects.create(building = building , user = user3 , user_points_in_building = 3)
        Leaderboard.objects.create(building = building , user = user4 , user_points_in_building = 4)
        Leaderboard.objects.create(building = building , user = user5 , user_points_in_building = 5)

        pp = ShopItem.objects.create(name='User', type = 'Profile Picture', cost = 0, availableForPurchase = False, image = 'static/shop_items/User.png')
        border = ShopItem.objects.create(name='Black Border', type = 'Border', cost = 0, availableForPurchase = False, image = 'static/shop_items/Black_Border.png')
        background = ShopItem.objects.create(name='White Background', type = 'Background', cost = 0, availableForPurchase = False, image = 'static/shop_items/White_Background.png')

        users = list(User.objects.all())
        for user_add in users:
            user_add.profile_pic = pp
            user_add.profile_border = border
            user_add.profile_background = background
            user_add.save()


    def tearDown(self):
        # Clean up run after every test method
        pass

    def test_get_leaderboard(self):
        # Test to see if the endpoint for getting leaderboard in a building
        c = Client()

        # Get leaderboard for 'test' building
        response = c.get('/leaderboard/test/')
        data = response.json().get('data')
        # Verify leaderboard should only have 5 entries
        self.assertEqual(5, len(data))

    def test_leaderboard_order(self):
        # Test that leaderboard is in correct order sorted by points
        c = Client()

        # Get leaderboard for 'test' building
        response = c.get('/leaderboard/test/')
        data = response.json().get('data')

        for i in range(5):
            # Verify points are in expected order
            expected = 5 - i
            self.assertEqual(data[i]['points'], expected)
            # Verify usernames are correct
            expected_username = 'unitTestUS' + str(expected)
            self.assertEqual(data[i]['username'], expected_username)

    def test_empty_leaderboard(self):
        # Test that empty leaderboards are handled correctly
        c = Client()

        # Get leaderboard for 'empty' building
        response = c.get('/leaderboard/empty/')
        data = response.json().get('data')
        self.assertEqual(data, [])

    def test_leaderboard_fake_building(self):
        # Test that leaderboard cannot be gotten for nonexistent building
        c = Client()

        # Get leaderboard for 'empty' building
        response = c.get('/leaderboard/zzzzzzzz/')
        # Verify response code is 404 not found
        self.assertEqual(response.status_code, 404)
