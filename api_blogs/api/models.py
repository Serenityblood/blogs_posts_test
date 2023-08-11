from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Blog(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='blog'
    )


class Post(models.Model):
    title = models.CharField(
        'Название',
        max_length=140,
        blank=False,
        null=False
    )
    pub_date = models.DateField(
        'Дата публикации',
        auto_now_add=True
    )
    blog = models.ForeignKey(
        Blog,
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Блог'
    )
    text = models.CharField(
        'Текст',
        max_length=140
    )

    class Meta:
        ordering = ('pub_date',)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscribing',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    blog = models.ForeignKey(
        Blog,
        related_name='subscribers',
        on_delete=models.CASCADE,
        verbose_name='Блог'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'blog'],
                name='unqiue_subscription'
            )
        ]


class Read(models.Model):
    user = models.ForeignKey(
        User,
        related_name='read',
        on_delete=models.CASCADE,
        verbose_name='Читатель'
    )
    post = models.ForeignKey(
        Post,
        related_name='who_read',
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unqiue_post'
            )
        ]
