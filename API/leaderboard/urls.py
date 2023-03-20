from django.urls import path

from . import views

# URL patterns for handling interactions with leaderboards
app_name = 'leaderboard'
urlpatterns = [
    path('<building_name>/', views.leaderboard, name='leaderboard'),
]