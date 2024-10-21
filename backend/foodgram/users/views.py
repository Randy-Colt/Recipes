from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import AvatarSerializer, SubscriptionSerializer
from users.models import Subscription


User = get_user_model()


class ProfileUserViewSet(UserViewSet):

    @action(detail=False,
            methods=('put', 'delete'),
            permission_classes=[IsAuthenticated],
            url_path='me/avatar')
    def avatar(self, request):
        if request.method == 'PUT':
            serializer = AvatarSerializer(request.user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        if not request.user.avatar:
            return Response(
                {'errors': 'Аватара не существует'},
                status=status.HTTP_400_BAD_REQUEST)
        request.user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
# можно ли изменить функцию post_or_delete(), чтобы она обрабатывала подписку?
    def subscribe(self, request, id):
        user = request.user
        author = self.get_object()
        if user.id == int(id):
            return Response(
                {'errors': 'Нельзя отписаться/подписаться на самого себя.'},
                status.HTTP_400_BAD_REQUEST
            )
        try:
            if request.method == 'DELETE':
                message = 'Вы уже отписались от этого пользователя.'
                Subscription.objects.get(user=user, author=author).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            message = 'Вы уже подписаны на этого пользователя.'
            Subscription.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(
                author, context={'request': request})
        except (Subscription.DoesNotExist, IntegrityError):
            return Response(
                {'errors': f'{message}'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        subs = User.objects.filter(subscribers__user=request.user)
        paginator = self.paginate_queryset(subs)
        serializer = SubscriptionSerializer(
            paginator, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
