from django.urls import path
from auths import views

urlpatterns = [
   path('register/', views.RegisterAPIView.as_view(), name='auth-register'),
]