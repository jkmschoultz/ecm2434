from database.models import Leaderboard, Building

'''
Methods for interaction with leaderboards
'''
def get_leaderboard(building_name):
    # Get the top 5 people in the leaderboard for a building
    building = Building.objects.get(name = building_name)
    # Get the leaderboard for the building
    leaderboard = Leaderboard.objects.filter(building=building).order_by('-user_points_in_building')
    # Make list of top 5 users with their corresponding points
    data = []
    for entry in leaderboard:
        data.append({
            'username': entry.user.username,
            'points': entry.user_points_in_building
        })
    # Return top 5 in leaderboard    
    return data[:5]
