from typing import Iterable
from django.db import models
from apps.security_agent.choices import LanguageChoices
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
    
    analyzer = models.ForeignKey("security_agent.Analyzer", on_delete=models.CASCADE)
    vulnerability = models.ForeignKey("vulnerabilities.Vulnerability", on_delete=models.CASCADE)
    meta_data = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

