from rest_framework import serializers

from foodgram.settings import SITE_URL
from recipes.models import Recipe


class MiniRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = f'{SITE_URL}{instance.image.url}'
        return representation
