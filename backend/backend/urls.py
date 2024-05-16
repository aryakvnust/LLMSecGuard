from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/', include('apps.auth.urls')),
    path('api/benchmark-agent/', include('apps.benchmark_agent.rest.urls')),
    path('api/prompt-agent/', include('apps.prompt_agent.rest.urls')),
    path('api/results/', include('apps.results.rest.urls')),
    path('api/security-agent/', include('apps.security_agent.rest.urls')),
    path('api/vulnerabilities/', include('apps.vulnerabilities.rest.urls')),
]
