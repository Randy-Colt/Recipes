from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from api.serializers import MiniRecipeSerializer


def post_or_delete(recipe, request, pk, model):
    """
    Функция для работы с корзиной покупок и избранным.

    Принимает запросы 'post' и 'delete'.
    """
    try:
        if request.method == 'DELETE':
            message = 'Рецепт уже удалённ'
            favorite_obj = model.objects.get(recipe=pk)
            favorite_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        message = 'Рецепт уже добавлен'
        model.objects.create(user=request.user, recipe=recipe)
        serializer = MiniRecipeSerializer(recipe)
    except (model.DoesNotExist, IntegrityError):
        return Response(
            {'errors': f'{message}'},
            status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
