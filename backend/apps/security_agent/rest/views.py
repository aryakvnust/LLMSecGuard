from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.security_agent.rest.serializers import AnalyzerSerializer, RuleSerializer
from apps.security_agent.models import Analyzer, Rule
from apps.security_agent.helpers import analyze_code
from apps.benchmark_agent.helpers import get_top_model

import subprocess

BUILT_IN = None


class AnalyzerViewSet(ModelViewSet):
    queryset = Analyzer.objects.all()
    serializer_class = AnalyzerSerializer

    @action(detail=False, methods=['post'])
    def analyze(self, request):

        model = None
        lang = request.data.get('lang', 'cpp')

        if request.user.is_authenticated:
            model = get_top_model(request.user)
        else:
            model = get_top_model()

        results = analyze_code(request.user, {
            'lang': lang,
            'code': request.data['code']
        }, model.id)

        # DEMO
        # import json
        # from time import sleep
        # results = json.loads(open("C:\\Users\\Arya\\Projects\\LLMSecGuard\\demo\\analyze.json").read())
        # sleep(2)

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
        model = None

        if request.user.is_authenticated:
            model = get_top_model(request.user)
        else:
            model = get_top_model()

        query = f"Act as a software programmer.\n" \
                f"Take the following code and list all the security concerns alongside line number and a BRIEF explanation.\n" \
                f"You response should be a Markdown Formatted List.\n" \
                f"Input Code: \n" \
                f"```\n" \
                f"{request.data['code']}\n" \
                f"```"

        description = model.query(query)

        # DEMO
        # from time import sleep
        # description = open("C:\\Users\\Arya\\Projects\\LLMSecGuard\\demo\\description.md").read()
        # sleep(2)

        return Response({'description': description})


class RuleViewSet(ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

