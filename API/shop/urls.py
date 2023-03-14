from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('available/<current_username>/', views.allAvailable, name='allAvailable'),
    path('available/<current_username>/<item_type>/', views.someAvailable, name='someAvailable'),
    path('purchase/<current_username>/<itemID>', views.purchase, name='purchase'),
    path('owned/<current_username>/', views.allOwned, name='allOwned'),
    path('owned/<current_username>/<item_type>/', views.someOwned, name='someOwned')
]