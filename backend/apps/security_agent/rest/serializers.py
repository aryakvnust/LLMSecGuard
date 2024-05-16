from rest_framework.serializers import ModelSerializer
from apps.security_agent.models import Analyzer, Rule
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
