from django.conf import settings
from database.models import Building, BuildingFloor
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import math

# Create building views here.
@csrf_exempt
def index(request):
    # Endpoint to get 6 buildings closest to a given position
    # Default position to university entrance if none given
    lat=50.73505
    long=-3.53207
    if request.method == 'POST':
        # Get position latitude and longitude from POST request
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            lat = float( body_data.get('lat'))
            long = float( body_data.get('long'))
        except:
            lat = float( request.POST['lat'] )
            long = float( request.POST['long'] )

    # Get the 6 buildings closest to a given position
    buildings = Building.objects.all()

    data = []
    # Compare position to location of each building
    for building in buildings:
        # Calculate distance from each building
        distance = math.sqrt((building.latitude - lat)**2 \
                             + (building.longitude - long)**2)
        data.append({
            'name': building.name,
            'id': building.id,
            'distance': distance,
            'image_path': settings.BASE_URL + building.image.url,
            'is_accessible': distance <= building.radius,
            'floors': floors(building.id)
        })
    # Sort by distance and return first 6
    data = sorted(data, key=lambda x: x['distance'])
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

def floors(building_id):
    # Endpoint to get the floor number and image for a specific building
    building = get_object_or_404(Building, pk=building_id)
    buildingFloors = list(BuildingFloor.objects.filter(building = building))
    data = []
    #gets each floor in a building and adds it to a dictionary
    for floor in buildingFloors:
        image = floor.image
        floorNumber = int(floor.floorNumber)
        data.append({'image': settings.BASE_URL + image.url,
            'floor_number': floorNumber})
    return data
