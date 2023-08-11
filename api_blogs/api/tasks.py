from django.contrib.auth import get_user_model

from api_blogs.celery import app
from .models import Post


User = get_user_model()


@app.task
def send_posts():
    for user in User.objects.all():
        posts = Post.objects.filter(
            blog__subscribers__user=user
        ).order_by('-id')[:5]
        print(f'{posts} отправлены {user}')
