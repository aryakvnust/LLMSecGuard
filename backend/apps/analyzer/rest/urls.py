from rest_framework.routers import DefaultRouter
from apps.analyzer.rest.views import AnalyzerViewSet, RuleViewSet, BenchmarkViewSet

router = DefaultRouter()
router.register(r'analyzer', AnalyzerViewSet)
router.register(r'rule', RuleViewSet)
router.register(r'benchmark', BenchmarkViewSet)

urlpatterns = router.urls