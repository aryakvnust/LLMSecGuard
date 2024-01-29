from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from requests import post, get
from .models import LLM, LLMSummary, Results, RecordedIssuws
from codeanalyzer.models import Engine

from django.db.models import Avg
from datetime import datetime, timedelta


class CreatePrompt(APIView):
    def get(self, request):
        # Logic for handling GET requests
        return render(request, 'promptdispatcher/prompt.html')

    def post(self, request):
        # model = LLM.objects.get(id=1)
        model = Results.get_top_model()
        code = request.data.get('code')
        query = request.data.get('prompt')
        noanalyze = request.data.get('noanalyze') == "true"
        
        if code is None:            
            query += "\n\n    Only return the code, don't include any other information,\n    such as a preamble or suffix.\n"
            code = model.get_model().query(query)
        
        # debug
        # debug = get("http://localhost:5000/analyze_code").json()
        # code = debug['code']
        # issues = debug['results']
        
        # issues = post("http://localhost:5000/analyze_code", json={
        #     "code": code,
        #     "language": "cpp"
        # }).json()
        
        if noanalyze:
            return render(request, "codeanalyzer/analyze.html", {'engines': Engine.objects.all(), 'code': code, 'lang': 'cpp'})
        
        issues = Engine.objects.get(id=1).dispatch('cpp', code)
        
        if len(issues) > 0:
            query_ = "Try to fix these vulnerabilities in the following code:\n"
            
            for issue in issues:
                query_ += "- '{}' at line {}\n".format(issue['description'], issue['line'])
                
            query_ += "\n\n```\n{}\n```".format(code)
            query_ += "\n\n    Only return the code, don't include any other information,\n    such as a preamble or suffix.\n"
            code = model.query(query_)
        
        result = Results.objects.create(
            model=model,
            issue_count=len(issues),
        )
        
        for issue in issues:
            RecordedIssuws.objects.create(
                result=result,
                issue=issue['cwe_id']
            )
        
        
        if request.query_params.get('api') is not None:
            return Response({
                'response': {
                    'code': code,
                    'issues': issues,
                },
            })
        else:
            return render(request, "promptdispatcher/code-analysis.html", {
                    'code': code,
                    'issues': issues,
                    'lang': 'cpp'
            })

class ScoreBoard(APIView):
    def get(self, request):
        last_month = datetime.now() - timedelta(days=30)
        results = Results.objects.filter(created_at__gte=last_month)
        average_issue_count = results.values('model').annotate(avg_issue_count=Avg('issue_count')).order_by('-avg_issue_count')
        
        max_count = max(map(lambda x: x['avg_issue_count'], average_issue_count))
        
        for i, aic in enumerate(average_issue_count):
            average_issue_count[i]['model'] = LLM.objects.get(id=aic['model'])
            average_issue_count[i]['score'] = (aic['avg_issue_count'] / max_count * 100)
            
        return render(request, 'promptdispatcher/scoreboard.html', {'aics': average_issue_count})
    
class LLMList(APIView):
    def get(self, request):
        if request.query_params.get('api') is not None:
            return Response(LLM.objects.all())
            
        return render(request, 'promptdispatcher/models.html', {'llms': LLM.objects.all()})
    
class LLMDetails(APIView):
    def get(self, request, llm_type):
        print(llm_type)
        if request.query_params.get('api') is not None:
            return Response(LLM.objects.all())
        
        
        return render(request, 'promptdispatcher/model.html', {
            'summary': LLMSummary.objects.get(model_type=llm_type),
            'llms': LLM.objects.filter(model__contains=llm_type)
        })