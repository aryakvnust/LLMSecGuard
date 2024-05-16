from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.prompt_agent.rest.serializers import LlmModelSerializer
from apps.prompt_agent.models import LlmModel
from apps.security_agent.helpers import analyze_code
from apps.prompt_agent.rest.permissions import IsPublicOrIsOwner


class LlmModelViewSet(ModelViewSet):
    queryset = LlmModel.objects.all()
    serializer_class = LlmModelSerializer
    permission_classes = [IsPublicOrIsOwner]
    
    
    @action(detail=True, methods=['post'])
    def query(self, request, pk=None):
        model = self.get_object()
        prompt = request.data['prompt']
        analyze = request.data.get('analyze', True)
        language = request.data.get('cpp', True)
        
        results = model.query(prompt)
        analysis = {}
        
        if analyze:
            analysis = analyze_code(request.user, {
                'lang': 'cpp' if language else 'python',
                'code': prompt
            }, model.id)            
        
        return Response({'results': results, 'analysis': analysis})

    @action(detail=True, methods=['post'])
    def summerize(self, request, pk=None):
        model = self.get_object()
        code = request.data['code']
        
        prompt = f"Summerize the following code and list any possible security concerns:\n{code}"
        prompt += "\n\n Your response should be markdown formatted: "
        
        return Response({'results': model.query(prompt)})


