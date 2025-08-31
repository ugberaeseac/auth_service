from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ForgotPasswordSerializer, ResetPasswordConfirmationSerializer


class RegisterAPIView(generics.GenericAPIView):
    # serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordAPIView(generics.GenericAPIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'If the email exists, a reset link has been sent'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordConfirmAPIView(generics.GenericAPIView):
    def post(self, request):
        serializer = ResetPasswordConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Your password has been reset'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


