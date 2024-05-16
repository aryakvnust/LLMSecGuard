from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError

from apps.benchmark_agent.rest.serializers import BenchmarkSerializer, MonthlySumCacheSerializer
from apps.benchmark_agent.choices import BenchmarkTypeChoices
from apps.benchmark_agent.models import History, Benchmark, MonthlySumCache
from apps.prompt_agent.models import LlmModel

from datetime import timedelta
from django.db.models import Sum

 
class BenchmarkViewSet(ModelViewSet):
    queryset = Benchmark.objects.all()
    serializer_class = BenchmarkSerializer

    @action(detail=False, methods=['get'])
    def overview(self, request):
        benchmarks = Benchmark.objects.all()
        last_benchmark = Benchmark.objects.last()
        benchmarks = Benchmark.objects.filter(created_at__gte=last_benchmark.created_at - timedelta(days=30))
        
        benchmarks = benchmarks.values('model', 'branch').annotate(
            metric1_sum=Sum('metric1'),
            metric2_sum=Sum('metric2'),
            metric3_sum=Sum('metric3'),
            metric4_sum=Sum('metric4'),
            metric5_sum=Sum('metric5')
        )

        data = []
        for benchmark in benchmarks:
            data.append(Benchmark(
                model = LlmModel.objects.get(id=benchmark['model']),
                branch = benchmark['branch'],
                metric1 = benchmark['metric1_sum'],
                metric2 = benchmark['metric2_sum'],
                metric3 = benchmark['metric3_sum'],
                metric4 = benchmark['metric4_sum'],
                metric5 = benchmark['metric5_sum']
            ))
            
            
        data = BenchmarkSerializer(data, many=True).data
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def chart_data(self, request):
        branch = request.query_params.get('branch', BenchmarkTypeChoices.STATS_PER_MODEL)
        
        
        keys = {
           'Injection_Successful_Count': Sum('metric1'),
           'Injection_Unsuccessful_Count': Sum('metric2'),
           'Total_Count': Sum('metric3'),
           'Injection_Successful_Percentage': Sum('metric4'),
           'Injection_Unsuccessful_Percentage': Sum('metric5'),
        }
        
        if branch == BenchmarkTypeChoices.PRIVILEGE_ESCALATION:
            keys = {
                'Is_Extremely_Malicious': Sum('metric1'),
                'Is_Potentially_Malicious': Sum('metric2'),
                'Is_Non_Malicious': Sum('metric3'),
                'Total_Count': Sum('metric4'),
                'Malicious_Percentage': Sum('metric5'),
            }
        
        benchmarks = Benchmark.objects.filter(branch=branch)
        benchmarks = benchmarks.values('model').annotate(
            **keys
        )
        
        return Response(benchmarks)

class MonthlySumCacheViewSet(ModelViewSet):
    queryset = MonthlySumCache.objects.all()
    serializer_class = MonthlySumCacheSerializer
    
    def get_queryset(self):
        model = self.request.query_params.get('model')
        query = super().get_queryset()
        
        if model is not None:
            query = query.filter(model__id=model)
            
        return query.order_by('date')
    
    @action(detail=False, methods=['get'])
    def chart_data(self, request):
        model = request.query_params.get('model')
        
        if model is None:
            raise ValidationError({'model': 'This field is required'}, code=400)
        
        data = MonthlySumCache.objects.filter(model__id=model).values('date').annotate(
            usage=Sum('usage'),
            errors=Sum('errors')
        )
        
        return Response(data)
