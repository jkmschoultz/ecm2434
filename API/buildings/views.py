from database.models import Building
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from . import buildings
import json

# Create building views here.
@csrf_exempt
def index(request):
    # Endpoint to get 6 buildings closest to a given position
    # Default position to university entrance if none given
    lat=50.73505
    long=-3.53207
    if request.method == 'POST':
        # Get position latitude and longitude from POST request
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        lat = float( body_data.get('lat'))
        long = float( body_data.get('long'))

    data = buildings.get_six_closest(lat, long)
    return JsonResponse({'data': data[:6]})

def detail(request, building_id):
    # Endpoint to get information for a specific building
    building = get_object_or_404(Building, pk=building_id)
    data = {
        'name': building.name,
        'latitude': building.latitude,
        'longitude': building.longitude
    }
    return JsonResponse(data)
