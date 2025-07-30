
from django.contrib import admin
from django.urls import path, include


from django.conf import settings


# from core_apps.user_auth.views import TestLoggingView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]
