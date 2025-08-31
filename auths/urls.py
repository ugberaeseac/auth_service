from django.urls import path
from auths import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
   #Auth
   path('login/', views.LoginAPIView.as_view(), name='auth-login'),
   path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),

   path('register/', views.RegisterAPIView.as_view(), name='auth-register'),
   path('password/forgot/', views.ForgotPasswordAPIView.as_view(), name='auth-forgot-password'),
   path('password/reset/', views.ResetPasswordConfirmAPIView.as_view(), name='auth-reset-password'),
]