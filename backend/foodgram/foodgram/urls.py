from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api.views import redirect_short_link

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', TemplateView.as_view(template_name='redoc.html')),
    path('api/', include('api.urls')),
    path('api/', include('users.urls')),
    path('s/<str:short_link>/', redirect_short_link,
         name='redirect_short_link'),
]
