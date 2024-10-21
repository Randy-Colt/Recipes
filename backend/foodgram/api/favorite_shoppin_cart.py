from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from api.minirecipe import MiniRecipeSerializer


def post_or_delete(instance, request, pk, model):
    """
    Функция для работы с корзиной покупок и избранным.

    Принимает запросы 'post' и 'delete'.
    """
    try:
        if request.method == 'DELETE':
            message = 'Рецепт уже удалённ'
            model.objects.get(recipe=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        message = 'Рецепт уже добавлен'
        model.objects.create(user=request.user, recipe=instance)
        serializer = MiniRecipeSerializer(instance)
    except (model.DoesNotExist, IntegrityError):
        return Response(
            {'errors': f'{message}'},
            status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status.HTTP_201_CREATED)
