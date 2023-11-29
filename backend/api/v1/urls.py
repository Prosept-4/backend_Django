from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from api.v1.views import AuthViewSet, TelegramTest
from users.views import CustomUserViewSet
from .views import (DealerViewSet,
                    PriceViewSet,
                    ProductViewSet,
                    MatchViewSet)

router = DefaultRouter()

router.register(r'users', CustomUserViewSet)
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'dealer', DealerViewSet)
router.register(r'dealer-price', PriceViewSet)
router.register(r'product', ProductViewSet)
router.register(r'match', MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(),
         name='login'),
    path('auth/logout/', AuthViewSet, name='logout'),
    path('telegram/', TelegramTest.as_view({'get': 'send'}), name='telegram'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
