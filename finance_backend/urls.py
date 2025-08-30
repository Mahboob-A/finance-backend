
from django.contrib import admin
from django.urls import path, include


from django.conf import settings

from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView, SpectacularSwaggerView


# from core_apps.user_auth.views import TestLoggingView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name='schema'),
    path("api/v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("api/v1/schema/redoc/", SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]



admin.site.site_header = "Finance Bank Backend Admin"
admin.site.site_title = "Finance Bank Backend Admin Portal"
admin.site.index_title = "Welcome to Finance Bank Backend Admin Portal"
