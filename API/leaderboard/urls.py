from django.urls import path

from . import views

# App for handling interactions with leaderboards
app_name = 'leaderboard'
urlpatterns = [
    path('<building_name>/', views.leaderboard, name='leaderboard'),
]