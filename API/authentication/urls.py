from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# App for registration and authentication of users
app_name = 'authentication'
urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.CreateUser.as_view(), name='create_user'),
    path('', views.GetUser.as_view(), name='authorize')
]