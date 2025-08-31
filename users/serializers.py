from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)
    class Meta:
        model = User
        fields = ('user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'created_at')
        read_only_fields = ('user_id', 'created_at')git 