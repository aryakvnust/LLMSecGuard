from rest_framework.serializers import ModelSerializer
from apps.analyzer.models import Analyzer, Rule, Benchmark, MonthlySumCache
from apps.analyzer.choices import BenchmarkTypeChoices
from apps.vulnerabilities.rest.serializers import VulnerabilitySerializer
from apps.prompt_agent.rest.serializers import LlmModelSerializer, LlmModelListSerializer

class AnalyzerSerializer(ModelSerializer):
    class Meta:
        model = Analyzer
        fields = '__all__'
        
class RuleSerializer(ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['objects'] = {
            'analyzer': AnalyzerSerializer(instance.analyzer).data,
            'vulnerability': VulnerabilitySerializer(instance.vulnerability).data
        }
        return data
    
class BenchmarkSerializer(ModelSerializer):
    class Meta:
        model = Benchmark
        fields = ['branch', 'model', 'created_at', 'updated_at']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if instance.branch == BenchmarkTypeChoices.PRIVILEGE_ESCALATION:
            data['is_extremely_malicious'] = instance.metric1
            data['is_potentially_malicious'] = instance.metric2
            data['is_non_malicious'] = instance.metric3
            data['total_count'] = instance.metric4
            data['malicious_percentage'] = instance.metric5
        else:
            data['injection_successful_count'] = instance.metric1
            data['injection_unsuccessful_count'] = instance.metric2
            data['total_count'] = instance.metric3
            data['injection_successful_percentage'] = instance.metric4
            data['injection_unsuccessful_percentage'] = instance.metric5
            
        
        data['objects'] = {
            'model': LlmModelSerializer(instance.model).data,
            'branch': BenchmarkTypeChoices(instance.branch).label
        }
        return data
    
class MonthlySumCacheSerializer(ModelSerializer):
    class Meta:
        model = MonthlySumCache
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['objects'] = {
            'model': LlmModelListSerializer(instance.model).data,
            'rate': instance.usage / (instance.usage + instance.errors) if instance.usage + instance.errors > 0 else 0
        }
        return data
