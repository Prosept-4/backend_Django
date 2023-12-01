from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from api.v1.views import AuthViewSet, AnalysisViewSet, PostponeViewSet, \
    NoMatchesViewSet
from users.views import CustomUserViewSet
from api.v1.views import (DealerViewSet,
                          DealerParsingViewSet,
                          ProductViewSet,
                          MatchViewSet)

router = DefaultRouter()

router.register(r'users', CustomUserViewSet)
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'dealer', DealerViewSet)
router.register(r'dealer-products', DealerParsingViewSet)
router.register(r'product', ProductViewSet)
router.register(r'match', MatchViewSet)
router.register(r'postpone', PostponeViewSet, basename='postpone')
router.register(r'has_no_matches', NoMatchesViewSet, basename='has_no_matches')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(),
         name='login'),
    path('auth/logout/', AuthViewSet, name='logout'),
    path('analyze/', AnalysisViewSet.as_view({'get': 'analyze'}), name='analyze'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
