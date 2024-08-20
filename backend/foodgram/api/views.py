from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import RecipeSerializer, TagSerializer
from recipes import models as recipes

User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    queryset = recipes.Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = recipes.Recipe.objects.all()
    serializer_class = RecipeSerializer
