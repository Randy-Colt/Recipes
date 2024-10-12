from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from foodgram.settings import SITE_URL
from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Tag)
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',


class Base64Serializer(serializers.ModelSerializer):
    pass


class MiniRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredients.id')
    name = serializers.CharField(source='ingredients.name')
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngredientRecipe
        exclude = ('recipe', 'ingredients')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(
        many=True, source='recipe_ingredients')
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = 'pub_date',

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        return False


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(write_only=True)


    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')
# TODO: заменить на константы
    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Убедитесь, что это значение больше либо равно 1'
            )
        return value


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('author', 'pub_date')

    def _unique_validation(self, value, message):
        value_list = []
        for item in value:
            if item in value_list:
                raise serializers.ValidationError(message)
            value_list.append(item)

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Убедитесь, что добавили ингридиент')
        self._unique_validation(ingredients, 'Ингридиенты не могут повторяться')
        return ingredients

    def validate_tags(self, tag):
        if not tag:
            raise serializers.ValidationError('Убедитесь, что добавили тег')
        self._unique_validation(tag, 'Теги не могут повторяться')
        return tag

    def _create_ingredients(self, recipe, ingredients):
        IngredientRecipe.objects.bulk_create(
            IngredientRecipe(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredients=ingredient['id']) for ingredient in ingredients
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context['request'].user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        self._create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', False)
        ingredients = validated_data.pop('ingredients', False)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)
        if ingredients:
            instance.ingredients.clear()
            self._create_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class ShortLinkSerializer(serializers.Serializer):
    short_link = serializers.CharField()

    def to_representation(self, instance):
        url = f'{SITE_URL}/s/{instance}'
        return {'short-link': url}
