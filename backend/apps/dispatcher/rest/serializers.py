from rest_framework.serializers import ModelSerializer
from apps.dispatcher.models import LlmModel

class LlmModelSerializer(ModelSerializer):
    class Meta:
        model = LlmModel
        fields = '__all__'
        