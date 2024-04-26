from rest_framework.serializers import ModelSerializer
from apps.vulnerabilities.models import Vulnerability

class VulnerabilitySerializer(ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__'
        