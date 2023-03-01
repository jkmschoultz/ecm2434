
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from database.models import Building, Leaderboard
import json

class LogAnswers(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        correct = int( body_data.get('correct'))
        building_id = int( body_data.get('building'))
        building = Building.objects.get(id=building_id)
        new_xp = correct * 5
        user.xp += new_xp
        user.bottles += 1
        leaderboard, created = Leaderboard.objects.get_or_create(building=building, user=user)
        leaderboard.user_points_in_building += new_xp
        user.save()
        leaderboard.save()
        return redirect('achievements:detail', current_username=user.username)