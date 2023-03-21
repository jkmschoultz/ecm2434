from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from database.models import Building, Leaderboard
import json

class LogAnswers(APIView):
    # Endpoint to register a user's answers to a quiz
    permission_classes = [IsAuthenticated]  # Can only register answers of an authenticated user

    def post(self, request):
        # Get data passed from POST
        user = request.user
        correct, building_name = '', ''
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            correct = int( body_data.get('correct'))
            building_name = str(body_data.get('building'))
        except:
            correct = int(request.POST['correct'])
            building_name = str(request.POST['building'])
        building = Building.objects.get(name=building_name)

        # Add 5 XP for every correct answer and increment number of bottles drank by user
        new_xp = correct * 5
        user.xp += new_xp
        # Create or add to user in leaderboard for building
        leaderboard, created = Leaderboard.objects.get_or_create(building=building, user=user)
        leaderboard.user_points_in_building += new_xp
        user.save()
        leaderboard.save()
        # Redirect to page listing any new achievements achieved by user
        return redirect('achievements:detail', current_username=user.username)