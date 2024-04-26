from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.auth.views import UserViewSet, SignupView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', UserViewSet)

# from apps.auth.views 

urlpatterns = [        
    path('sign-up/', SignupView.as_view(), name='sign-up'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
