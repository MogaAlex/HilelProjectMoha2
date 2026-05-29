from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from shop.api.views import (CategoryViewSet,
                                ProductViewSet,
                                GetTokenPairView,
                                OrderViewSet,
                                CartViewSet)




router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cart', CartViewSet, basename='cart')

app_name = 'shop_api'

urlpatterns = [
    path('', include(router.urls)),
    path('get-token/', GetTokenPairView.as_view(), name='jwt_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='shop_api:schema'), name='swagger-ui'),
]