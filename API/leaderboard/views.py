from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from database.models import Leaderboard,Building
from django.conf import settings

# Create leaderboard views here
def leaderboard(request, building_name):
    # Get the leaderboard of top 5 from a building name
    building = get_object_or_404(Building, name=building_name)
    # Get the leaderboard for the building
    leaderboard = Leaderboard.objects.filter(building=building).order_by('-user_points_in_building')
    # Make list of top 5 users with their corresponding points
    data = []
    for entry in leaderboard:
        data.append({
            'username': entry.user.username,
            'points': entry.user_points_in_building,
            'border': settings.BASE_URL + entry.user.profile_border.image.url,
            'profile_pic': settings.BASE_URL + entry.user.profile_pic.image.url
        })
    # Return json of top 5 in leaderboard
    return JsonResponse({'data': data[:5]})