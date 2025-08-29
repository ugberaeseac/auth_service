from django.urls import path
from users import views

urlpatterns = [
   path('', views.UserListAPIView.as_view(), name='user-list'),
   path('<uuid:user_id>/', views.UserDetailAPIView.as_view(), name='user-detail'),
]