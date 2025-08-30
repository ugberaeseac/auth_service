from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .serializers import UserSerializer
from .models import User


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]



class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'

    def get_object(self):
        user = super().get_object()
        if self.request.user == user or self.request.user.is_staff:
            return user
        else:
            raise PermissionDenied({'detail': 'You do not have the permission to access this user'})




