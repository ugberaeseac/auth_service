from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User

class UsersAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="admin@admin.com",
            username="admin",
            password="Adminpass123",
            first_name="Admin",
            last_name="User",
            is_staff=True,
        )
        
        self.alice = User.objects.create_user(
            email="alice@demo.com",
            username="alice",
            password="Alicepass123",
            first_name="Alice",
            last_name="Demo",
        )
        self.bob = User.objects.create_user(
            email="bob@demo.com",
            username="bob",
            password="Bobpass123",
            first_name="Bob",
            last_name="Demo",
        )
        self.list_url = reverse("user-list")


    def test_user_list_requires_admin_status(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.alice)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)


    def test_user_retrieves_self_but_others_forbidden(self):
        detail_url = reverse("user-detail", kwargs={"user_id": self.alice.user_id})
       
        self.client.force_authenticate(self.alice)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "alice@demo.com")

        self.client.force_authenticate(self.bob)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # staff user allowed and can retrieve all user detail
        self.client.force_authenticate(self.admin)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_update_self_details_successful(self):
        url = reverse("user-detail", kwargs={"user_id": self.alice.user_id})
        self.client.force_authenticate(self.alice)
        response = self.client.patch(url, {"first_name": "Alicia"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Alicia")
