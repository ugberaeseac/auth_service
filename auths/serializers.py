from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
import secrets


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'created_at')
        read_only_fields = ('user_id', 'created_at')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def save(self):
        email = self.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return # For security - if user doesn't exist, don't reveal valid emails

        if user:
            user_id = user.user_id
            token = secrets.token_urlsafe(32)
            key = f'pwdreset:{user_id}'
            
            cache.set(key, token, timeout=600)
            reset_link = f'http://127.0.0.1:8000/api/auth/password/reset/?user_id={user_id}&token={token}'

            subject = f'Password Rest Request for {user.email}'
            message = f"""
            Hello {user.first_name},

            You requested a password reset. Click below to set a new password:

            {reset_link}

            if you didn't request this, please ignore this email.
            """

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
 


class ResetPasswordConfirmationSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    def validate(self, value):
        user_id = value.get('user_id')
        token = value.get('token')

        key = f'pwdreset:{user_id}'
        cached_token = cache.get(key)

        if cached_token != token or cached_token is None:
            raise serializers.ValidationError({'token': 'Invalid or expired token'})
        return value

    
    def save(self):
        user_id = self.validated_data.get('user_id')
        new_password = self.validated_data.get('new_password')
        key = f'pwdreset:{user_id}'

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({'user_id': 'Invalid User ID'})

        if user:
            user.set_password(new_password)
            user.save()
            cache.delete(key)
            return user
    