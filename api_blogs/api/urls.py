from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BlogViewSet, PostViewSet,
    ReadView, SubscribeView,
    UserViewSet
)


app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'blogs', BlogViewSet, basename='blogs')


urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'blogs/<int:id>/subscribe/',
        SubscribeView.as_view(),
        name='subscription'
    ),
    path(
        'posts/<int:id>/read/',
        ReadView.as_view(),
        name='read'
    )
]
