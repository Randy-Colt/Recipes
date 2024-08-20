from rest_framework import serializers

from recipes import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipe
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.CharField

    class Meta:
        model = models.IngredientRecipe
        fields = ('recipe', 'ingredients', 'amount')
