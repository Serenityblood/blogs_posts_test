from django.contrib import admin

from .models import Blog, Post, Read, Subscription

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Read)
admin.site.register(Subscription)
