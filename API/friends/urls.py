from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'friends'
urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('allFriends', views.allFriends.as_view(), name='allFriends'),
    path('allPending', views.allPending.as_view(), name='allPending')
    ##path('request', views.request.as_view(), name='request'),
    ##path('accept', views.accept.as_view(), name='accept')
]