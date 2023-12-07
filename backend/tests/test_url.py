from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class AuthURLsTestCase(APITestCase):
    def setUp(self):
        """Create test_user"""
        self.user = get_user_model().objects.create_user(
            email='example@name.ru',
            password='example_password',
            first_name='example_first_name',
            last_name='example_last_name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=None)

    def test_login_url(self):
        """Test user login."""
        response = self.client.post('/api/auth/login/', {
            'email': 'example@name.ru',
            'password': 'example_password'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_logout_url(self):
        """Test user logout."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_token_verify_url(self):
        """Test user token verify."""
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            '/api/auth/token/verify/',
            {'token': str(refresh.access_token)}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh_url(self):
        """Test user token refresh."""
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            '/api/auth/token/refresh/',
            {'refresh': str(refresh)}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
