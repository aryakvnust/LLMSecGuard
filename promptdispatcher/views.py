from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from CybersecurityBenchmarks.benchmark import llm
from requests import post, get
from .models import LLM, Results

class CreatePrompt(APIView):
    def get(self, request):
        # Logic for handling GET requests
        return render(request, 'promptdispatcher/prompt.html')

    def post(self, request):
        # model = LLM.objects.get(id=1)
        model = Results.get_top_model()
        code = request.data.get('code')
        query = request.data.get('prompt')
        
        
        if code is None:            
            query += "\n\n    Only return the code, don't include any other information,\n    such as a preamble or suffix.\n"
            code = model.get_model().query(query)
        
        # debug
        # debug = get("http://localhost:5000/analyze_code").json()
        # code = debug['code']
        # issues = debug['results']
        
        issues = post("http://localhost:5000/analyze_code", json={
            "code": code,
            "language": "cpp"
        }).json()
        
        # if len(issues) > 0:
        #     query_ = "Try to fix these vulnerabilities in the following code:\n"
            
        #     for issue in issues:
        #         query_ += "- '{}' at line {}\n".format(issue['description'], issue['line'])
                
        #     query_ += "\n\n```\n{}\n```".format(code)
        #     query_ += "\n\n    Only return the code, don't include any other information,\n    such as a preamble or suffix.\n"
        #     code = model.query(query_)
        
        
        
        
        Results.objects.create(
            model=model,
            issue_count=len(issues),
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

