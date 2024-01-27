from django.urls import path
from .views import AnalyzeCode

urlpatterns = [
    path('', AnalyzeCode.as_view(), name='analyze_code')
]
