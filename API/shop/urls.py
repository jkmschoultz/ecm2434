from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('available/<current_username>/', views.allAvailable, name='allAvailable'),
    path('available/<current_username>/<item_type>/', views.someAvailable, name='someAvailable'),
    path('purchase/<current_username>/<item_name>', views.purchase, name='purchase'),
    path('owned/<current_username>/', views.allOwned, name='allOwned'),
    path('owned/<current_username>/<item_type>/', views.someOwned, name='someOwned'),
    path('auth-available/', views.AuthAllAvailable.as_view(), name='authAllAvailable'),
    path('auth-available/<item_type>/', views.AuthSomeAvailable.as_view(), name='authSomeAvailable'),
    path('auth-purchase/', views.AuthPurchase.as_view(), name='authPurchase'),
    path('auth-owned/', views.AuthAllOwned.as_view(), name='authAllOwned'),
    path('auth-owned/<item_type>/', views.AuthSomeOwned.as_view(), name='authSomeOwned')
]