from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from CybersecurityBenchmarks.insecure_code_detector import insecure_code_detector as icd


import json

# Create your views here.

class AnalyzeCode(APIView):
    def get(self, request):
        return render(request, 'codeanalyzer/analyze.html')

    def post(self, request):
        return Response({
            'response': 'code'
        })