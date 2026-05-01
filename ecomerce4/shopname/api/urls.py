from django.urls import include, path
from rest_framework.routers import DefaultRouter
from shopname.api.views import CategoryViewSet, ProductViewSet, GetTokenPairView

# from ecomerce2.shopname.api.views import ProductViewSet

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

app_name = 'shopname_api'

urlpatterns = [
    path('', include(router.urls)),
    path('get-token/', GetTokenPairView.as_view(), name='jwt_token'),
]