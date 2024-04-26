from rest_framework.routers import DefaultRouter
from apps.results.rest.views import ResultViewSet

router = DefaultRouter()
router.register(r'result', ResultViewSet)

urlpatterns = router.urls