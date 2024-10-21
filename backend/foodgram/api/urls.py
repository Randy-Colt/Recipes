from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router_v1 = DefaultRouter()

router_v1.register('tags', views.TagViewSet)
router_v1.register('recipes', views.RecipeViewSet)
router_v1.register('ingredients', views.IngredientViewSet)

urlpatterns = [
    path('recipes/download_shopping_cart/', views.download_shopping_cart),
    path('', include(router_v1.urls)),
]
