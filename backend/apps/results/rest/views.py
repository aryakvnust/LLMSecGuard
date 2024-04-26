from rest_framework.viewsets import ModelViewSet

from apps.results.rest.serializers import ResultSerializer
from apps.results.models import Result

class ResultViewSet(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    
