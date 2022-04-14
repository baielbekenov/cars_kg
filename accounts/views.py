from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

User = get_user_model()
from rest_framework import status, response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from .service import send_message


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_message(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)


class ActivateUserAccount(APIView):
    def get(self, request, activation_code):
        user = User.objects.get(activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return render(request, 'index.html', locals())


class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return response.Response({
                'token': token.key
            })


class LogoutAPIView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

