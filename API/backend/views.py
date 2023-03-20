from django.http import JsonResponse
from datetime import datetime

def index(request):
    # The base index page for the django backend API
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d/%m/%Y")

    data = {
        'time': current_time,
        'date': current_date,
    }
    # Returns data for simple verification of a connection to the backend
    return JsonResponse(data)