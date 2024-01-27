from django.db import models
from CybersecurityBenchmarks.benchmark import llm
from django.db.models import Avg
from datetime import datetime, timedelta

# Create your models here.

supported_models = (
    "ANYSCALE::meta-llama/Llama-2-13b-chat-hf",
)

class LLM(models.Model):
    model = models.CharField(max_length=100, choices=[(model, model) for model in supported_models])
    api_key = models.CharField(max_length=100)
    
    def get_model(self):
        identifier = "::".join([self.model, self.api_key])
        model = llm.create(identifier)
        return model
    
    def __str__(self) -> str:
        return self.model
        
    
class Results(models.Model):
    model = models.ForeignKey(LLM, on_delete=models.CASCADE)
    issue_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def get_top_model():
        last_month = datetime.now() - timedelta(days=30)
        results = Results.objects.filter(created_at__gte=last_month)
        average_issue_count = results.values('model').annotate(avg_issue_count=Avg('issue_count')).order_by('-avg_issue_count').first()
        return LLM.objects.get(id=average_issue_count['model'])
