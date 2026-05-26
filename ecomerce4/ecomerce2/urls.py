"""
URL configuration for ecomerce2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from payments.views import checkout_view
from shop_chat.views import register

from django.urls import path

def trigger_error(request):
    division_by_zero = 1 / 0


def health_check(request):
    status_data = {
        "status": "healthy",
        "services": {
            "database": "up",
            "redis_cache": "up"
        }
    }
    has_errors = False

    try:
        connections['default'].cursor()
    except OperationalError:
        status_data["services"]["database"] = "down"
        has_errors = True

    try:
        cache.set("__health_check__", 1, timeout=5)
        if not cache.get("__health_check__"):
            raise Exception("Redis unreachable")
    except Exception:
        status_data["services"]["redis_cache"] = "down"
        has_errors = True

    if has_errors:
        status_data["status"] = "unhealthy"
        return JsonResponse(status_data, status=500)

    return JsonResponse(status_data, status=200)


def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shopname.urls')),
    path('', include('payments.urls')),
    path('chat/', include('shop_chat.urls')),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/<int:order_id>/', checkout_view, name='checkout_order'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('register/', register, name='register'),
    path('api/', include('shopname.api.urls', namespace='shopname_api')),
    path('api-token-obtain/', obtain_auth_token, name='api_token_obtain'),
    path('api-token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sentry-debug/', trigger_error),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)