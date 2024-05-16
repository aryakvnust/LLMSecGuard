from rest_framework.routers import DefaultRouter
from apps.benchmark_agent.rest.views import BenchmarkViewSet, MonthlySumCacheViewSet

router = DefaultRouter()
router.register(r'benchmark', BenchmarkViewSet)
router.register(r'monthly-sum-cache', MonthlySumCacheViewSet)

urlpatterns = router.urls