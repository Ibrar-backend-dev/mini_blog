from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from .utils import generate_email_verification_token

User = get_user_model()


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_creates_unverified_user_and_sends_verification(self):
        response = self.client.post(
            "/auth/signup/",
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "strongPass123",
                "password_confirm": "strongPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "testuser")
        self.assertFalse(response.data["is_email_verified"])
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_unverified_user_cannot_login(self):
        user = User.objects.create_user(
            username="testuser2",
            email="user2@example.com",
            password="strongPass123",
        )
        user.is_email_verified = False
        user.save(update_fields=["is_email_verified"])

        response = self.client.post(
            "/auth/login/",
            {"username_or_email": "user2@example.com", "password": "strongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Email is not verified.", str(response.data))

    def test_logout_blacklists_refresh_token(self):
        user = User.objects.create_user(
            username="testuser4",
            email="user4@example.com",
            password="strongPass123",
        )
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        response = self.client.post(
            "/auth/login/",
            {"username_or_email": "user4@example.com", "password": "strongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        refresh_token = response.data["refresh"]

        logout_response = self.client.post(
            "/auth/logout/",
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.data["detail"], "Successfully logged out.")

    def test_verify_email_endpoint_updates_user(self):
        user = User.objects.create_user(
            username="testuser3",
            email="user3@example.com",
            password="strongPass123",
        )
        user.is_email_verified = False
        user.save(update_fields=["is_email_verified"])

        token = generate_email_verification_token(user)
        response = self.client.get(f"/auth/verify-email/{token}/")

        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.is_email_verified)

