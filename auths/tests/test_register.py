from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User



class RegisterAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("auth-register")
        self.payload = {
            "email": "testuser@test.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
        }

    def test_user_registration_successful(self):
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="testuser@test.com").exists())
        user = User.objects.get(email="testuser@test.com")
        self.assertTrue(user.check_password(self.payload["password"]))
        
        self.assertNotIn("password", response.data) # password must not be returned in response

    
    def test_cannot_set_admin_fields_from_payload(self):
        payload = {**self.payload, "is_staff": True, "is_superuser": True}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="testuser@test.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    
    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            email=self.payload["email"],
            username="testuser2",
            password="newpass123",
            first_name="Newtest",
            last_name="User",
        )
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
