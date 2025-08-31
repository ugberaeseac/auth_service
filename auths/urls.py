from django.urls import path
from auths import views

urlpatterns = [
   path('register/', views.RegisterAPIView.as_view(), name='auth-register'),
   path('password/forgot/', views.ForgotPasswordAPIView.as_view(), name='auth-forgot-password'),
   path('password/reset/', views.ResetPasswordConfirmAPIView.as_view(), name='auth-reset-password'),
]