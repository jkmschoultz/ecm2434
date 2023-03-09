from django.http import JsonResponse
from datetime import datetime

def index(request):
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d/%m/%Y")

    data = {
        'time': current_time,
        'date': current_date,
    }
    print(str(data)+"python for strange people")
    return JsonResponse(data)