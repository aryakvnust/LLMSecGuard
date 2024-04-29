from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.analyzer.rest.serializers import AnalyzerSerializer, RuleSerializer, BenchmarkSerializer
from apps.analyzer.choices import BenchmarkTypeChoices
from apps.analyzer.models import Analyzer, Rule, History, Benchmark
from apps.dispatcher.models import LlmModel

import requests
import subprocess
from datetime import timedelta
from django.db.models import Sum

BUILT_IN = None

class AnalyzerViewSet(ModelViewSet):
    queryset = Analyzer.objects.all()
    serializer_class = AnalyzerSerializer
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        analyzers = Analyzer.objects.filter(is_public=True)
        model = LlmModel.objects.get(id=1)
        
        if request.user.is_authenticated:
            analyzers = analyzers | Analyzer.objects.filter(user=request.user)
        
        
        results = []
        saved = []
        rules = {}
        fix = None
        
        for analyzer in analyzers:
            
            for rule in analyzer.rule_set.all():
                rules[rule.id] = rule
                
            result = requests.post(analyzer.url, json={
                'lang': request.data['lang'],
                'code': request.data['code'],
                'rules': [{ 
                    'id': rule.id,
                    'rule': rule.rule
                } for rule in rules.values()]
            })
                
            for res in result.json()['results']:
                line = res['line']
                rule = res['rule']
                
                if (line, rule) in saved:
                    continue
                
                saved.append((line, rule))
                results.append({
                    'code': res['code'],
                    'line': res['line'],
                    'rule': RuleSerializer(rules[res['rule']]).data
                })
                
                History.objects.create(
                    rule=rules[res['rule']],
                    model=model
                )

        if len(results) > 0:
            query = f"""
                Fix these vulnerabilities in the following code:\n
            """
            
            for res in results:
                print("===== RES: ", res)
                query += "- " + res['rule']['name'] + "(" + res['rule']['description'] + ") at line " + str(res['line']) + "\n"
                
            query += "\n\n    Only return the code, DONT'T include any other information,\n    such as a preamble or suffix.\n"
            
            fix = model.query(query)
            fix = fix.strip()
        
        return Response({'results': results, 'fix': fix})
    
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