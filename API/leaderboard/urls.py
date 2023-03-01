from django.urls import path

from . import views

app_name = 'leaderboard'
urlpatterns = [
    path('<building_name>/', views.leaderboard, name='leaderboard'),
]