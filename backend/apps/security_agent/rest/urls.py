from rest_framework.routers import DefaultRouter
from apps.security_agent.rest.views import AnalyzerViewSet, RuleViewSet

router = DefaultRouter()
router.register(r'analyzer', AnalyzerViewSet)
router.register(r'rule', RuleViewSet)

urlpatterns = router.urls