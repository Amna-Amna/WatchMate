from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from watchlist_app import models
from django.core.cache import cache


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        self.stream_platform = models.StreamPlatform.objects.create(name='Netflix', about='Netflix is a streaming service that offers a wide variety of TV shows and movies.', website='https://www.netflix.com')
        

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

    def test_stream_platform_list(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=[self.stream_platform.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.stream_platform = models.StreamPlatform.objects.create(name='Netflix', about='Netflix is a streaming service that offers a wide variety of TV shows and movies.', website='https://www.netflix.com')
        self.watchlist = models.WatchList.objects.create(title='Test Movie', story_line='Test story line', active=True, platform=self.stream_platform)
        self.review = models.Review.objects.create(review_user=self.user, watchlist=self.watchlist, rating=5, description='Initial review')
       
    def test_watchlist_create_forbidden(self):
        data = {
            'title': 'Test Movie',
            'story_line': 'Test story line',
            'active': True,
            'platform': self.stream_platform.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_create_as_staff(self):
        self.user.is_staff = True
        self.user.save()
        data = {
            'title': 'Test Movie',
            'story_line': 'Test story line',
            'active': True,
            'platform': self.stream_platform.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('single-watchlist', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_update(self):
        data = {
            'title': 'Test Movie',
            'story_line': 'Test story line',
            'active': True,
            'platform': self.stream_platform.id
        }
        self.user.is_staff = True
        self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(reverse('single-watchlist', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_delete(self):
        self.user.is_staff = True
        self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(reverse('single-watchlist', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewTestCase(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.stream_platform = models.StreamPlatform.objects.create(name='Netflix', about='Netflix is a streaming service that offers a wide variety of TV shows and movies.', website='https://www.netflix.com')
        self.watchlist = models.WatchList.objects.create(title='Test Movie', story_line='Test story line', active=True, platform=self.stream_platform)

    def test_review_create_forbidden(self):
        data = {
            'rating': 5,
            'description': 'Test description',
            'watchlist': self.watchlist.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_create_as_staff(self):
        data = {
            'rating': 5,
            'description': 'Test description',
            'watchlist': self.watchlist.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 1)
        self.assertEqual(models.Review.objects.get().rating, 5)

        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You have already reviewed this watchlist!', str(response.data))
        
    def test_review_list(self):
        review = models.Review.objects.create(review_user=self.user, watchlist=self.watchlist, rating=4, description='Initial')
        response = self.client.get(reverse('review-list', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        review = models.Review.objects.create(review_user=self.user, watchlist=self.watchlist, rating=4, description='Initial')
        response = self.client.get(reverse('review-detail', args=[self.watchlist.id, review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_update(self):
        review = models.Review.objects.create(review_user=self.user, watchlist=self.watchlist, rating=4, description='Initial')
        data = {
            'rating': 4,
            'description': 'Test description',
            'watchlist': self.watchlist.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(reverse('review-detail', args=[self.watchlist.id, review.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_delete(self):
        review = models.Review.objects.create(review_user=self.user, watchlist=self.watchlist, rating=4, description='Initial')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(reverse('review-detail', args=[self.watchlist.id, review.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_user_review(self):
        response = self.client.get(reverse('user-review', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_user_review_query_params(self):
        response = self.client.get(reverse('user-review-query-params'), {'username': self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        