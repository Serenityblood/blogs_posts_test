from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .models import Blog, Post, Subscription


class BlogPostTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='test1')
        self.user2 = User.objects.create(username='test2')
        self.blog1 = Blog.objects.create(user=self.user1)
        self.blog2 = Blog.objects.create(user=self.user2)
        token = AccessToken.for_user(self.user1)
        self.client.force_authenticate(user=self.user1, token=token)

    def test_posts_creation(self):
        response = self.client.post(
            '/api/posts/',
            data={
                'title': 'title',
                'text': 'text',
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.first().title, 'title')
        self.assertEqual(Post.objects.first().blog, self.blog1)

    def test_subscription_create(self):
        response = self.client.post(
            f'/api/blogs/{self.user2.blog.id}/subscribe/'
        )
        self.assertEqual(response.status_code, 201)

    def test_postsfeed_create(self):
        Post.objects.create(title='title', text='text', blog=self.blog2)
        Subscription.objects.create(user=self.user1, blog=self.blog2)
        response = self.client.get('/api/users/postsfeed/')
        self.assertEqual(
            len(response.data.get('results')), 1
        )
