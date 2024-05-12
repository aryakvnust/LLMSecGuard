from typing import Iterable
from django.db import models
from apps.analyzer.choices import LanguageChoices, BenchmarkTypeChoices
import requests
import json
import datetime

# Create your models here.

class Analyzer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    url = models.URLField(max_length=100)
    api_key = models.CharField(max_length=100, blank=True, null=True)
    
    summary = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.name

class Rule(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rule = models.TextField()
    language = models.CharField(max_length=3, choices=LanguageChoices.choices, default=LanguageChoices.C)
    
    analyzer = models.ForeignKey("analyzer.Analyzer", on_delete=models.CASCADE)
    vulnerability = models.ForeignKey("vulnerabilities.Vulnerability", on_delete=models.CASCADE)
    meta_data = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class History(models.Model):
    model = models.ForeignKey("prompt_agent.LlmModel", on_delete=models.CASCADE)
    rule = models.ForeignKey("analyzer.Rule", on_delete=models.CASCADE)
    
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
