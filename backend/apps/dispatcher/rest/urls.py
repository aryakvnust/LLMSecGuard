from rest_framework.routers import DefaultRouter
from apps.dispatcher.rest.views import LlmModelViewSet

router = DefaultRouter()
router.register(r'models', LlmModelViewSet)

urlpatterns = router.urls