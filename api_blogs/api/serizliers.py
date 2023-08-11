from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Blog, Post, Read, Subscription
from .validators import validate_username


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'blog', 'username')


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_SIZE,
        validators=[validate_username]
    )
    password = serializers.CharField(
        validators=[validate_password]
    )


class PostSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'blog', 'is_read')

    def get_is_read(self, post):
        request = self.context.get('request')
        return (
            request
            and request.user.read.filter(post=post).exists()
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

    class Meta:
        model = Blog
        fields = ('id', 'user', 'blog')


class ReadSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Read
        fields = ('user', 'post')


class BlogSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('user', 'posts', 'is_subscribed')

    def get_posts(self, blog):
        posts = blog.posts.all().order_by('-pub_date')
        return PostSerializer(posts, many=True).data

    def get_is_subscribed(self, blog):
        request = self.context.get('request')
        return (request
                and Subscription.objects.filter(
                    user=request.user, blog=blog
                ).exists())
