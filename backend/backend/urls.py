from django.contrib import admin
from django.urls import path, include
from .views import index
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),

    path('docs/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/auth/', include('apps.auth.urls')),
    path('api/benchmark-agent/', include('apps.benchmark_agent.rest.urls')),
    path('api/prompt-agent/', include('apps.prompt_agent.rest.urls')),
    path('api/results/', include('apps.results.rest.urls')),
    path('api/security-agent/', include('apps.security_agent.rest.urls')),
    path('api/vulnerabilities/', include('apps.vulnerabilities.rest.urls')),
]
