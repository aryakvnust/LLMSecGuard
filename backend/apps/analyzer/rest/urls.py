from rest_framework.routers import DefaultRouter
from apps.analyzer.rest.views import AnalyzerViewSet, RuleViewSet, BenchmarkViewSet, MonthlySumCacheViewSet

router = DefaultRouter()
router.register(r'analyzer', AnalyzerViewSet)
router.register(r'rule', RuleViewSet)
router.register(r'benchmark', BenchmarkViewSet)
router.register(r'monthly-sum-cache', MonthlySumCacheViewSet)

urlpatterns = router.urls