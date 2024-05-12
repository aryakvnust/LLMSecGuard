from rest_framework.serializers import ModelSerializer
from apps.prompt_agent.models import LlmModel

class LlmModelSerializer(ModelSerializer):
    class Meta:
        model = LlmModel
        fields = '__all__'
        
class LlmModelListSerializer(ModelSerializer):
    class Meta:
        model = LlmModel
        fields = ['id', 'name', 'created_at', 'updated_at']
        