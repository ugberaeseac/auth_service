from django.urls import path
from auths import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
   #Auth
   path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('register/', views.RegisterAPIView.as_view(), name='auth-register'),
   path('password/forgot/', views.ForgotPasswordAPIView.as_view(), name='auth-forgot-password'),
   path('password/reset/', views.ResetPasswordConfirmAPIView.as_view(), name='auth-reset-password'),
]