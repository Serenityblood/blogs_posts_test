from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Blog, Post, Read, Subscription
from .paginators import CustomPaginator
from .serizliers import (
    BlogSerializer, PostSerializer, ReadSerializer,
    SignUpSerializer, SubscriptionSerializer, UserSerializer
)


User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(['POST'], False)
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                password=make_password(serializer.validated_data['password'])
            )
            Blog.objects.get_or_create(user=user)
        except IntegrityError as error:
            error_text = f'{error}'
            if 'username' in error_text:
                message = 'Такой юзернейм уже занят'
            return Response(
                {'message': message}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['GET', 'PATCH', 'DELETE'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            if user.check_password(request.data.get('current_password')):
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'Неправильный пароль'},
                            status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False,
            permission_classes=(IsAuthenticated,),
            pagination_class=CustomPaginator)
    def postsfeed(self, request):
        posts = Post.objects.filter(
            blog__subscribers__user=request.user
        ).order_by('-id')
        if posts.count() > 500:
            posts[:500]
        posts = self.paginate_queryset(posts)
        return self.get_paginated_response(
            PostSerializer(posts, many=True).data
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        return serializer.save(blog=self.request.user.blog)


class SubscribeView(views.APIView):
    def post(self, request, id):
        if not request.user:
            return Response(
                {'message': 'Нужна аутентификация'},
                status=status.HTTP_403_FORBIDDEN
            )
        subscription = Subscription.objects.get_or_create(
            user=request.user, blog=get_object_or_404(Blog, id=id)
        )
        serializer = SubscriptionSerializer(
            subscription, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        if not request.user:
            return Response(
                {'message': 'Нужна аутентификация'},
                status=status.HTTP_403_FORBIDDEN
            )
        get_object_or_404(
            Subscription,
            user=request.user,
            blog=get_object_or_404(Blog, id=id)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReadView(views.APIView):
    def post(self, request, id):
        if not request.user:
            return Response(
                {'message': 'Нужна аутентификация'},
                status=status.HTTP_403_FORBIDDEN
            )
        read = Read.objects.get_or_create(
            user=request.user, post=get_object_or_404(Post, id=id)
        )
        serializer = ReadSerializer(
            read, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        if not request.user:
            return Response(
                {'message': 'Нужна аутентификация'},
                status=status.HTTP_403_FORBIDDEN
            )
        get_object_or_404(
            Read,
            user=request.user,
            post=get_object_or_404(Post, id=id)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
