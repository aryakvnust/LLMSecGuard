from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError

from apps.analyzer.rest.serializers import AnalyzerSerializer, RuleSerializer, BenchmarkSerializer, MonthlySumCacheSerializer
from apps.analyzer.choices import BenchmarkTypeChoices
from apps.analyzer.models import Analyzer, Rule, History, Benchmark, MonthlySumCache
from apps.dispatcher.models import LlmModel
from apps.analyzer.helpers import analyze_code

import subprocess
from datetime import timedelta
from django.db.models import Sum

BUILT_IN = None

class AnalyzerViewSet(ModelViewSet):
    queryset = Analyzer.objects.all()
    serializer_class = AnalyzerSerializer
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        model = LlmModel.objects.get(id=1)
        lang = request.data.get('lang', 'cpp')
        
        results = analyze_code(request.user, {
            'lang': lang,
            'code': request.data['code']
        }, model.id)
        
        
        return Response(results)
    
    @action(detail=False)
    def start_built_in(self, request):
        global BUILT_IN
        
        if BUILT_IN is not None:
            return Response({'message': 'Built-in analyzer is already running'})
        
        BUILT_IN = subprocess.Popen(["python", "services/analyzer/service.py"])
        return Response({'pid': BUILT_IN.pid})
    
    @action(detail=False)
    def stop_built_in(self, request):
        global BUILT_IN
        
        if BUILT_IN is None:
            return Response({'message': 'Built-in analyzer is not running'})
        
        BUILT_IN.terminate()
        BUILT_IN = None
        return Response({'message': 'Built-in analyzer stopped'})
    
    @action(detail=False, methods=['post'])
    def judge(self, request):
        model = LlmModel.objects.get(id=1)
        
        query = f"""
            Act as a software programmer. 
            
            Take the following code and list all the security concerns alongside line number and a BRIEF explanation.
            
            You response should be a Markdown Formatted List.
            
            Input Code: 
            ```
            {request.data['code']}
            ```
        """
        
        description = model.query(query)
        
        return Response({'description': description})
    
    
class RuleViewSet(ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    
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
            
        return query
    
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
