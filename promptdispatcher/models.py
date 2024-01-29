from django.db import models
from CybersecurityBenchmarks.benchmark import llm
from django.db.models import Avg
from datetime import datetime, timedelta

# Create your models here.

supported_models = (
    "ANYSCALE::meta-llama/Llama-2-13b-chat-hf",
)

model_types = [m.split("::")[1].split("/")[0] for m in supported_models]

class LLM(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100, choices=[(model, model) for model in supported_models])
    api_key = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def get_model(self):
        identifier = "::".join([self.model, self.api_key])
        model = llm.create(identifier)
        return model
    
    def get_type(self):
        return self.model.split("::")[1].split("/")[0]
    
    def get_summary(self):
        return LLMSummary.objects.get(model_type=self.get_type())
    
    def __str__(self) -> str:
        return self.name
        
class LLMSummary(models.Model):
    model_type = models.CharField(max_length=100, choices=[(m, m) for m in model_types], unique=True)
    summary = models.TextField()
    description = models.TextField()
    
class Results(models.Model):
    model = models.ForeignKey(LLM, on_delete=models.CASCADE)
    issue_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    benchmark = models.BooleanField(default=False)
    
    @staticmethod
    def get_top_model():
        last_month = datetime.now() - timedelta(days=30)
        results = Results.objects.filter(created_at__gte=last_month)
        average_issue_count = results.values('model').annotate(avg_issue_count=Avg('issue_count')).order_by('-avg_issue_count').first()
        return LLM.objects.get(id=average_issue_count['model'])
    
class RecordedIssuws(models.Model):
    issue = models.CharField(max_length=100)
    result = models.ForeignKey(Results, on_delete=models.CASCADE)
