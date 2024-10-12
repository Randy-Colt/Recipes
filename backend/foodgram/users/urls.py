from django.urls import include, path
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()

# router_v1.register('users', , basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
