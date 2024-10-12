from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('tags', views.TagViewSet)
router.register('recipes', views.RecipeViewSet)

urlpatterns = [
    path('recipes/download_shopping_cart/', views.download_shopping_cart),
    path('', include(router.urls)),
]
