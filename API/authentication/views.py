from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUser
from rest_framework.permissions import AllowAny
from rest_framework import status, exceptions
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from database.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

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
