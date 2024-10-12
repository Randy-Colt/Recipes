from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from api.favorite_shoppin_cart import post_or_delete
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    RecipeCreateSerializer, RecipeSerializer,
    ShortLinkSerializer, TagSerializer)
from recipes.models import (
    Favorite, Ingredient, IngredientRecipe,
    Recipe, ShoppingCart, ShortLinkConverter, Tag)

User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = IsAuthorOrReadOnly,

    # def get_queryset(self):
    #     queryset = recipes.Recipe.objects.select_related('author').prefetch_related(
    #         'ingredientrecipe__ingredients', 'tags'
    #     )

    #     return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(detail=True,
            permission_classes=[AllowAny],
            url_path='get-link')
    def get_link(self, request, pk):
        """Получить короткую ссылку."""
        recipe = self.get_object()
        short_link = ShortLinkConverter.objects.get(recipe=recipe).short_link
        serializer = ShortLinkSerializer(short_link)
        return Response(serializer.data)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return post_or_delete(self.get_object(), request, pk, Favorite)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return post_or_delete(self.get_object(), request, pk, ShoppingCart)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    user = request.user
    try:
        query_list = ShoppingCart.objects.filter(user=user)\
            .values('recipe__ingredients__name',
                    'recipe__ingredients__measurement_unit')\
            .annotate(amount_sum=Sum('recipe__recipe_ingredients__amount'))
    except ShoppingCart.DoesNotExist:
        return Response({'errors': 'Корзина пуста'},
                        status=status.HTTP_400_BAD_REQUEST)
    ingredients = 'Список покупок: \n'  # уверен, можно оптимизировать без строк
    for item in query_list:
        ingredients += (
            f'{item["recipe__ingredients__name"]} - '
            f'{item["amount_sum"]} '
            f'{item["recipe__ingredients__measurement_unit"]}\n'
        )
    filename = 'shopping_list.txt'
    response = HttpResponse(ingredients, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def redirect_short_link(request, short_link):
    """Перенаправить на url рецепта."""
    link_obj = get_object_or_404(
        ShortLinkConverter, short_link=short_link)
    return redirect('recipe-detail', f'{link_obj.recipe.pk}',  permanent=True)
