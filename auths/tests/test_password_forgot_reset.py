from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.core import mail
from django.core.cache import cache
import uuid
import secrets


class ForgotPasswordTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@demo.com",
            first_name="Test",
            last_name="User",
            password="OldPass123"
        )
        self.url = reverse("auth-forgot-password")

    def test_forgot_password_sends_email_if_user_exists(self):
        response = self.client.post(self.url, {"email": "testuser@demo.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Password Reset Request", mail.outbox[0].subject)

    def test_forgot_password_with_email_that_dont_exist(self):
        response = self.client.post(self.url, {"email": "fakeuser@demo.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
        self.assertEqual(len(mail.outbox), 0)


class ResetPasswordTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser2",
            email="testuser2@demo.com",
            first_name="Test",
            last_name="User",
            password="OldPass123"
        )
        self.url = reverse("auth-reset-password")

        self.token = secrets.token_urlsafe(32)
        cache.set(f"pwdreset:{self.user.user_id}", self.token, timeout=600)

    def test_reset_password_with_valid_token(self):
        payload = {
            "user_id": str(self.user.user_id),
            "token": self.token,
            "new_password": "NewPass123"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123"))

    def test_reset_password_with_invalid_token(self):
        payload = {
            "user_id": str(self.user.user_id),
            "token": "a_wrongtoken",
            "new_password": "NewPass123"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_with_invalid_user(self):
        payload = {
            "user_id": str(uuid.uuid4()),
            "token": self.token,
            "new_password": "NewPass123"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
