from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = 'name',

    # def filter_name(self, queryset, name, value):
    #     starts = queryset.filter(name__istartswith=value)
    #     contains = queryset.filter(
    #         name__icontains=value).exclude(name__istartswith=value)
    #     return starts.union(contains, all=True)


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_favorited_and_shopping_cart',
        field_name='favorites'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_favorited_and_shopping_cart',
        field_name='shopping_list'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_favorited_and_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        if value:
            lookup = '__'.join((name, 'user'))
            return queryset.filter(**{lookup: user})
        return queryset
