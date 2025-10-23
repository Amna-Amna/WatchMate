from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_stream_platform_create_forbidden(self):
        data = {
            'name': 'Netflix',
            'about': 'Netflix is a streaming service that offers a wide variety of TV shows and movies.',
            'website': 'https://www.netflix.com'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('stream-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_create_as_staff(self):
        self.user.is_staff = True
        self.user.save()
        data = {
            'name': 'Netflix',
            'about': 'Netflix is a streaming service that offers a wide variety of TV shows and movies.',
            'website': 'https://www.netflix.com'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('stream-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    