from database.models import Leaderboard , Building


class LeaderBoardRef:
    def getTopTen(building_name):
        building = Building.objects.get(name = building_name)
        building_points = Leaderboard.objects.get(building = building)
        top_ten = list(building_points.objects.order_by("user_points_in_building")[:5])
        return top_ten
