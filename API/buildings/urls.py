from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'buildings'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:building_id>/', views.detail, name='detail'),
    path('<building_name>/leaderboard/', views.getTopFive, name='getTopFive'),
]
