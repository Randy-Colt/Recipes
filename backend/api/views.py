from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from api.favorite_shopping_cart import delete_from_list, post_in_list
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer, RecipeCreateSerializer, RecipeSerializer,
    ShortLinkSerializer, TagSerializer)
from recipes.models import (
    Favorite, Ingredient, Recipe, ShoppingCart, ShortLinkConverter, Tag)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = DjangoFilterBackend,
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = IsAuthorOrReadOnly,
    filter_backends = DjangoFilterBackend,
    filterset_class = RecipeFilter

    def get_queryset(self):
        return Recipe.objects.select_related('author').prefetch_related(
            'recipe_ingredients__ingredients', 'tags')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(detail=True,
            permission_classes=[AllowAny],
            url_path='get-link')
    def get_link(self, request, pk):
        """Получить короткую ссылку."""
        short_link = get_object_or_404(
            ShortLinkConverter, recipe=pk).short_link
        serializer = ShortLinkSerializer(short_link)
        return Response(serializer.data)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        if request.method == 'DELETE':
            return delete_from_list(pk, Favorite)
        return post_in_list(self.get_object(), request, Favorite)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'DELETE':
            return delete_from_list(pk, ShoppingCart)
        return post_in_list(self.get_object(), request, ShoppingCart)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    try:
        query_list = request.user.shopping_list.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(amount_sum=Sum('recipe__recipe_ingredients__amount'))
    except ShoppingCart.DoesNotExist:
        return Response({'errors': 'Корзина пуста'},
                        status.HTTP_400_BAD_REQUEST)
    ingredients = ['Список покупок:']
    for item in query_list:
        ingredients.append(
            f'{item["recipe__ingredients__name"]} - '
            f'{item["amount_sum"]} '
            f'{item["recipe__ingredients__measurement_unit"]}'
        )
    ingredients = '\n'.join(ingredients)
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
    return redirect('recipe-detail', f'{link_obj.recipe.pk}', permanent=True)
