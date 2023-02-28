from database.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt

# Create authentication views here.
@csrf_exempt
def login(request):
    username, password = '', ''
    # Get provided login details
    if request.method == 'POST':
        # body_unicode = request.body.decode('utf-8')
        # body_data = json.loads(body_unicode)
        # username = str( body_data.get('username'))
        # password = str( body_data.get('password'))
        username = str( request.POST['username'])
        password = str( request.POST['password'])
    
    # Return empty if no login details provided
    if not username or not password:
        return JsonResponse({})
    
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return JsonResponse({})
    
    if user:
        payload = {
            'id': user.id,
            'username': user.username
        }
        jwt_token = jwt.encode(payload, "SECRET_KEY")
        return JsonResponse({'jwt_token', jwt_token})
    