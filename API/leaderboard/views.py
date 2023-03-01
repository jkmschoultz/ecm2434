import math
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from database.models import Leaderboard, Building

def leaderboard(request, building_name):
    building = get_object_or_404(Building, name=building_name)
    leaderboard = Leaderboard.objects.filter(building=building).order_by('-user_points_in_building')
    data = []
    for entry in leaderboard:
        data.append({
            'username': entry.user.username,
            'points': entry.user_points_in_building
        })
    return JsonResponse({'data': data})