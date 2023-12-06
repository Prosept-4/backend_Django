from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test.client import Client

 
class AuthURLsTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя в базе данных
        self.user = get_user_model().objects.create_user(
            email='example@name.ru',
            password='example_password',
            first_name='example_first_name',
            last_name='example_last_name',
        )
        self.client = APIClient()
        
    def test_login_url(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'example@name.ru',
            'password': 'example_password'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Извлекаем токен из ответа и устанавливаем его в HTTP_AUTHORIZATION
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def test_logout_url(self):        
        response = self.client.post('/api/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_verify_url(self):
        response = self.client.post('/api/auth/token/verify/', {'token': 'access_token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_refresh_url(self):
        response = self.client.post('/api/auth/token/refresh/', {'refresh': 'refresh_token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
        
