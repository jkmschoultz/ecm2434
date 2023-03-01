from django.urls import path

from . import views

app_name = 'achievements'
urlpatterns = [
    path('<current_username>/', views.all, name='all'),
    path('check/<current_username>/', views.detail, name='detail'),
]