from django.urls import path

from . import views

##End points for user data
app_name = 'users'
urlpatterns = [
    ##Endpoint for all user data
    path('<current_username>/', views.getUserProfileData, name='name'),
    ##Endpoint for verifing the users account
    path('<current_username>/verify', views.verifyAccount, name='name'),
    ##Endpoint for adding xp for when a user filles a bottle
    path('<current_username>/fillBottle', views.bottleFilled, name='name'),
    ##Endpoint for setting a users name
    path('<current_username>/setName/<new_name>', views.setName, name='name'),
    ##Endpoint for registering a user
    path('register/', views.index, name='name'),
]