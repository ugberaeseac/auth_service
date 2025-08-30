from rest_framework import serializers
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'created_at')
        read_only_fields = ('user_id', 'created_at')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


 