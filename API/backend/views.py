from django.http import JsonResponse
from datetime import datetime

def index(request):
    current_time = datetime.now().strftime("%-I:%S %p")
    current_date = datetime.now().strftime("%A %m %-Y")

    data = {
        'time': current_time,
        'date': current_date,
    }
    print(str(data)+"python for strange people")
    return JsonResponse(data)