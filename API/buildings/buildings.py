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
