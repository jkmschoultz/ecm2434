from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

class CreateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUser(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                refresh = RefreshToken.for_user(newuser)
                return JsonResponse({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                })
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        return redirect('users:getUserProfileData', current_username=username)