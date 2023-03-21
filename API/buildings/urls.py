from django.urls import path

from . import views

# URL patterns for handling interactions with buildings
app_name = 'buildings'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:building_id>/', views.detail, name='detail'),
]
