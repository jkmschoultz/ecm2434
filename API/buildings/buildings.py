from django.conf import settings
from database.models import Building, Leaderboard
import math

'''
Methods for interacting with buildings
'''
def get_six_closest(latitude, longitude):
    # Get the 6 buildings closest to a given position
    buildings = Building.objects.all()

    data = []
    # Compare position to location of each building
    for building in buildings:
        # Calculate distance from each building
        distance = math.sqrt((building.latitude - latitude)**2 + (building.longitude - longitude)**2)
        data.append({
            'name': building.name,
            'id': building.id,
            'distance': distance,
            'image_path': settings.BASE_URL + building.image.url,
            'is_accessible': distance <= building.radius
        })
    # Sort by distance and return first 6
    data = sorted(data, key=lambda x: x['distance'])
    return data[:6]

def get_leaderboard(building_name):
    # Get the top 5 people in the leaderboard for a building
    building = Building.objects.get(name = building_name)
    print(building_name)
    # Get the leaderboard for the building
    building_points = Leaderboard.objects.filter(building = building)
    top_five = list(building_points.order_by("user_points_in_building")[:5])
    # Make list of top 5 users with their corresponding points
    points = []
    names = []
    for leader in top_five:
            names.append(leader.user.name)
            points.append(leader.user_points_in_building)
    # Return tuple of list of names with corresponding points in leaderboard
    return names, points