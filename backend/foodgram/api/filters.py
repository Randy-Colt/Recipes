from django_filters.rest_framework import CharFilter, FilterSet

from recipes.models import Ingredient, Recipe

class IngredientFilter(FilterSet):
    name = CharFilter

    class Meta:
        model = Ingredient