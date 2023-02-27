from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('<current_username>/', views.getUserProfileData, name='name'),
]