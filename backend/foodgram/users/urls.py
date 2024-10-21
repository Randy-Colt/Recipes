from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views


router_v1 = DefaultRouter()

router_v1.register('users', views.ProfileUserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
