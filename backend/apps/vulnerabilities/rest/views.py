from rest_framework.viewsets import ModelViewSet

from apps.vulnerabilities.rest.serializers import VulnerabilitySerializer
from apps.vulnerabilities.models import Vulnerability

class VulnerabilityViewSet(ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    
