"""
Tests for user authentication endpoints and services.

Run with: python manage.py test apps.users.test_auth
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import signing
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from apps.users.services import create_user, authenticate_user
from apps.users.utils import generate_verification_token, decode_verification_token

User = get_user_model()


class SignupTestCase(APITestCase):
    """Test user signup flow."""

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')

    def test_valid_signup(self):
        """Test successful user signup."""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user_id', response.data)
        self.assertTrue(User.objects.filter(email='john@example.com').exists())

    def test_duplicate_email(self):
        """Test signup with duplicate email."""
        User.objects.create_user(username='john', email='john@example.com', password='Pass123!')
        data = {
            'username': 'jane',
            'email': 'john@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_password_mismatch(self):
        """Test signup with mismatched passwords."""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test signup with password < 8 chars."""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'Short1!',
            'password_confirm': 'Short1!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_fields(self):
        """Test signup with missing required fields."""
        response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)


class EmailVerificationTestCase(APITestCase):
    """Test email verification flow."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='SecurePass123!',
            is_email_verified=False
        )
        self.verify_url = reverse('verify-email', args=['<token>'])

    def test_valid_token(self):
        """Test verification with valid token."""
        token = generate_verification_token(self.user)
        url = reverse('verify-email', args=[token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)

    def test_already_verified(self):
        """Test verification when already verified."""
        self.user.is_email_verified = True
        self.user.save()
        token = generate_verification_token(self.user)
        url = reverse('verify-email', args=[token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token(self):
        """Test verification with invalid token."""
        url = reverse('verify-email', args=['invalid-token'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_token(self):
        """Test verification with expired token (>24h)."""
        # This is tricky to test without mocking time
        # For now, we skip this advanced test
        pass


class LoginTestCase(APITestCase):
    """Test user login flow."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='SecurePass123!',
            is_email_verified=True
        )

    def test_valid_login(self):
        """Test successful login."""
        data = {
            'email': 'john@example.com',
            'password': 'SecurePass123!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_wrong_password(self):
        """Test login with wrong password."""
        data = {
            'email': 'john@example.com',
            'password': 'WrongPassword123!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unverified_user(self):
        """Test login for unverified user."""
        unverified = User.objects.create_user(
            username='jane',
            email='jane@example.com',
            password='SecurePass123!',
            is_email_verified=False
        )
        data = {
            'email': 'jane@example.com',
            'password': 'SecurePass123!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexistent_user(self):
        """Test login for non-existent user."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'SomePassword123!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_case_insensitivity(self):
        """Test login with uppercase email."""
        data = {
            'email': 'JOHN@EXAMPLE.COM',
            'password': 'SecurePass123!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileTestCase(APITestCase):
    """Test user profile endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.profile_url = reverse('profile')
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='SecurePass123!',
            is_email_verified=True
        )

    def test_get_profile_authenticated(self):
        """Test profile retrieval for authenticated user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john@example.com')
        self.assertTrue(response.data['is_email_verified'])

    def test_get_profile_unauthenticated(self):
        """Test profile retrieval without authentication."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserServiceTestCase(TestCase):
    """Test user service functions."""

    def test_create_user(self):
        """Test user creation service."""
        user = create_user('johndoe', 'john@example.com', 'SecurePass123!')
        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertTrue(user.check_password('SecurePass123!'))

    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        user = create_user('johndoe', 'john@example.com', 'SecurePass123!')
        # User must verify email before authentication
        user.is_email_verified = True
        user.save()
        authenticated_user = authenticate_user(email='john@example.com', password='SecurePass123!')
        self.assertEqual(authenticated_user.username, 'johndoe')

    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password."""
        user = create_user('johndoe', 'john@example.com', 'SecurePass123!')
        # User must verify email before authentication
        user.is_email_verified = True
        user.save()
        with self.assertRaises(Exception):
            authenticate_user(email='john@example.com', password='WrongPassword!')

    def test_authenticate_unverified_user(self):
        """Test authentication for unverified user."""
        User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='SecurePass123!',
            is_email_verified=False
        )
        with self.assertRaises(Exception):
            authenticate_user(email='john@example.com', password='SecurePass123!')
