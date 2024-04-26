from rest_framework.routers import DefaultRouter
from apps.vulnerabilities.rest.views import VulnerabilityViewSet

router = DefaultRouter()
router.register(r'vulnerability', VulnerabilityViewSet)

urlpatterns = router.urls