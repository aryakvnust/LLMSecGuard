from django.db import models
from apps.benchmark_agent.choices import BenchmarkTypeChoices

import datetime

# Create your models here.

class History(models.Model):
    model = models.ForeignKey("prompt_agent.LlmModel", on_delete=models.CASCADE)
    rule = models.ForeignKey("security_agent.Rule", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.code

class MonthlySumCache(models.Model):
    model = models.ForeignKey("prompt_agent.LlmModel", on_delete=models.CASCADE)
    date = models.CharField(max_length=7)
    usage = models.PositiveBigIntegerField(default=0)
    errors = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.date
    
    def save(self, *args, **kwargs) -> None:
        
        if self.pk is None:
            self.date = datetime.date.today().strftime('%Y-%m')
        return super().save(*args, **kwargs)

class Benchmark(models.Model):
    branch = models.CharField(max_length=2, choices=BenchmarkTypeChoices.choices)
    model = models.ForeignKey("prompt_agent.LlmModel", on_delete=models.CASCADE)
    
    metric1 = models.FloatField()
    metric2 = models.FloatField()
    metric3 = models.FloatField()
    metric4 = models.FloatField()
    metric5 = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.branch} - {self.model}"

