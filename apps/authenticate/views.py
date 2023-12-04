from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserRegistrationSerializer,
    ActivationSerializer,
)


class RegistrationView(APIView):
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data='Спасибо за регистрацию! Вам было вычлано писмо с активационным кодом.',
                status=status.HTTP_201_CREATED

            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActivationView(APIView):
    def post(self, request: Request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate_account()
        return Response(
            'Аккаунт активирован!',
            status=status.HTTP_200_OK
            )
