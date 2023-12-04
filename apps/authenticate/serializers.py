from rest_framework import serializers 
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_lenght=100, required=True)
    email = serializers.EmailField(max_lenght=200, required=True)
    password = serializers.CharField(max_lenght=128, required=True)
    password_confrim = serializers.CharField(max_lenght=128, required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Этот ник уже занятб выбирите другой.'
            )
        return username
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Данный почтовый адресс уже занятб используйте другой.'
            )
        return email
    
    def validate(self, attrs: dict):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirm')
        if password != password_confirmation:
            raise serializers.ValidationError(
                "Пароли не совподают."
            )
        return attrs
    
    def create(self, validate_data:dict):
        user = User.objects.create_user(**validate_data)
        user.create_activation_code()
        user.send_activation_code()
        return user

class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=1, max_length=10, required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            return email
        raise serializers.ValidationError('user not ofund')
    
    def validate_code(self, code):
        if User.objects.filter(code=code).exists():
            raise serializers.ValidationError('code unknown')
        return code
    
    def validate(self, attrs:dict):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('user not foiunt')
        return attrs

    def activate_account(self):
        """ method for activatiom """
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.is_active = ''
        user.save()

