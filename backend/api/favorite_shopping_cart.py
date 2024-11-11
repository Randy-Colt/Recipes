from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from api.minirecipe import MiniRecipeSerializer


def post(instance, request, model):
    """
    Функция для добавления в корзину покупок или избранное.

    Принимает запросы 'post'.
    """
    try:
        model.objects.create(user=request.user, recipe=instance)
        serializer = MiniRecipeSerializer(instance)
        return Response(serializer.data, status.HTTP_201_CREATED)
    except IntegrityError:
        return Response(
            {'errors': 'Рецепт уже добавлен'},
            status=status.HTTP_400_BAD_REQUEST)


def delete(pk, model):
    """
    Функция для удаления из корзины покупок или избранного.

    Принимает запросы 'delete'.
    """
    try:
        model.objects.get(recipe=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except model.DoesNotExist:
        return Response(
            {'errors': 'Рецепт уже удалённ'},
            status=status.HTTP_400_BAD_REQUEST)
