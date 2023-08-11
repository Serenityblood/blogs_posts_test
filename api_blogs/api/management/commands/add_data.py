from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from mixer.backend.django import mixer

from api.models import Blog, Post, Subscription


User = get_user_model()

first_user = User.objects.get(id=1)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in mixer.cycle(100).blend(User):
            blog = Blog.objects.create(user=user)
            Subscription.objects.create(user=first_user, blog=blog)
            mixer.cycle(3).blend(Post, blog=blog)
