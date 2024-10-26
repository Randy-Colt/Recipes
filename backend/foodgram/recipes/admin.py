from django.contrib import admin

from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'image', 'added_in_favorites')
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = 'tags',
    readonly_fields = 'added_in_favorites',

    @admin.display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = 'name',
    ordering = 'name',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    ordering = 'name',


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(IngredientRecipe)
class IngredientRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredients', 'amount')
