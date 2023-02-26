import math
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse

from database.models import Building

# Create building views here.
def index(request):
    # Default position to Uni entrance if none given
    lat=50.73505
    long=-3.53207
    if request.method == 'POST':
        lat = float( request.POST['lat'] )
        long = float( request.POST['long'] )
        print(lat)
        print(long)

    # Calculate distance from each building
    buildings = Building.objects.values()
    for building in buildings:
        distance = math.sqrt((building['latitude'] - lat)**2 + (building['longitude'] - long)**2)
        building['distance'] = distance
        building['is_accessible'] = distance <= building['radius']
    # Sort by distance
    buildings = sorted(buildings, key=lambda x: x['distance'])
    for building in buildings:
        # Remove redundant fields
        del building['id']
        del building['latitude']
        del building['longitude']
        del building['radius']
        del building['distance']
    return JsonResponse({'data': buildings[:6]})

def detail(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    data = {
        'name': building.name,
        'latitude': building.latitude,
        'longitude': building.longitude
    }
    return JsonResponse(data)
