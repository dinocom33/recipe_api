"""
Tests for the User API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a new user."""

    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating a user with a valid payload is successful."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test that the password must be more than 5 characters."""

        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for valid user."""

        user_details = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test name'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""

        create_user(email='test@example.com', password='testpass123')
        payload = {
            'email': 'test@example.com',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_password(self):
        """Test that token is not created if password is missing."""

        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test name'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
