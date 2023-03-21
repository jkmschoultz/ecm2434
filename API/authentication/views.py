from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

from database.models import UserItem, ShopItem

class CreateUser(APIView):
    # An endpoint for creating a user in the app, returns the access and refresh token for the user
    permission_classes = [AllowAny]  # Allow anyone to create a user

    def post(self, request):
        # Use serializer to create user from data in POST
        reg_serializer = RegisterUser(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                # Unlocks the standard items for a user
                UserItem.objects.create(user = newuser, item = ShopItem.objects.get(name = 'User'))
                UserItem.objects.create(user = newuser, item = ShopItem.objects.get(name = 'Black Border'))
                UserItem.objects.create(user = newuser, item = ShopItem.objects.get(name = 'White Background'))
                refresh = RefreshToken.for_user(newuser)
                return JsonResponse({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                })
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUser(APIView):
    # Endpoint to trial getting an authenticated user
    permission_classes = [IsAuthenticated]

    # Return id of authenticated user making request
    def post(self, request):
        username = request.user.username
        return redirect('users:getUserProfileData', current_username=username)