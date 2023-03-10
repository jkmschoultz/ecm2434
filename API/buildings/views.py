from database.models import Building
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import json
import math

# Create building views here.
@csrf_exempt
def index(request):
    # Default position to Uni entrance if none given
    lat=50.73505
    long=-3.53207
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        lat = float( body_data.get('lat'))
        long = float( body_data.get('long'))
        print(lat)
        print(long)

    buildings = Building.objects.all()
    data = []
    for building in buildings:
        # Calculate distance from each building
        distance = math.sqrt((building.latitude - lat)**2 + (building.longitude - long)**2)
        data.append({
            'name': building.name,
            'id': building.id,
            'distance': distance,
            'image_path': settings.BASE_URL + 'buildings' + building.image.url,
            'is_accessible': distance <= building.radius
        })
    # Sort by distance
    data = sorted(data, key=lambda x: x['distance'])
    return JsonResponse({'data': data[:6]})

def detail(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    data = {
        'name': building.name,
        'latitude': building.latitude,
        'longitude': building.longitude
    }
    return JsonResponse(data)

def getTopFive(request, building_name):
        building = Building.objects.get(name = building_name)
        print(building_name)
        building_points = Leaderboard.objects.filter(building = building)
        top_ten = list(building_points.order_by("user_points_in_building")[:5])
        points = []
        names = []
        for leader in top_ten:
             names.append(leader.user.name)
             points.append(leader.user_points_in_building)
        return JsonResponse({'names': names, 'points':points})
