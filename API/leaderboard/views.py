from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from leaderboard.leaderboard import get_leaderboard

from database.models import Building

# Create leaderboard views here
def leaderboard(request, building_name):
    # Get the leaderboard of top 5 from a building name
    building = get_object_or_404(Building, name=building_name)
    leaderboard = get_leaderboard(building_name)
    # Return json of leaderboard data
    return JsonResponse({'data': leaderboard})