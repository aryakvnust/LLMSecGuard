from django.db import models
from requests import post, get, put, patch

# Create your models here.

http_methods = (
    "POST",
    "GET",
    "PUT",
    "PATCH",
)

http_body = (
    "JSON",
    "FORMDATA"
)

default_engines = (
    "WEGGLI",
    "REGEX",
    "SEMGREP"
)

class Engine(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, null=True, blank=True)
    api_type = models.CharField(max_length=100, choices=[(method, method) for method in http_methods])
    api_data = models.CharField(max_length=100, choices=[(body, body) for body in http_body])
    api_params = models.JSONField(max_length=100, null=True, blank=True)
    public = models.BooleanField(default=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    @staticmethod
    def get_useable_engines(user):
        return Engine.objects.filter(public=True) | Engine.objects.filter(user=user)
    
    def dispatch(self, language, code, user=None):
        dispatcher = None
        headers = {}
        params = self.api_params
        json = None
        data = None
        
        if self.api_key:
            headers['api-key'] = self.api_key
            
        patterns = InsecurePattern.get_useable_patterns(user=user)
        patterns = [{
            "description": pattern.description,
            "cwe_id": pattern.cwe_id,
            "rule": pattern.rule,
            "severity": pattern.severity,
            "analyzer": pattern.analyzer.lower(),
            "regexes": pattern.regexes,
            "pattern_id": pattern.pattern_id,
        } for pattern in patterns]
            
            
        if self.api_type == "POST":
            dispatcher = post
        elif self.api_type == "GET":
            dispatcher = get
        elif self.api_type == "PUT":
            dispatcher = put
        elif self.api_type == "PATCH":
            dispatcher = patch
            
        if self.api_data == "JSON":
            json = {
                "code": code,
                "language": language,
                "patterns": patterns
            }
        elif self.api_data == "FORMDATA":
            data = {
                "code": code,
                "language": language,
                "patterns": patterns
            }
            

        return dispatcher(self.api_url, json=json, data=data, headers=headers, params=params).json()
    

    def __str__(self) -> str:
        return self.name
    
    
class InsecurePattern(models.Model):
    description = models.CharField(max_length=100)
    cwe_id = models.CharField(max_length=100)
    rule = models.CharField(max_length=100)
    severity = models.CharField(max_length=100)
    regexes = models.JSONField(null=True, blank=True)
    pattern_id = models.CharField(max_length=100, null=True, blank=True)
    public = models.BooleanField(default=True)
    analyzer = models.CharField(max_length=100, choices=[(engine, engine) for engine in default_engines])
    approved = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    @staticmethod
    def get_useable_patterns(user=None):
        public_patterns = InsecurePattern.objects.filter(public=True, approved=True) 
        
        if user is not None: 
            public_patterns = public_patterns | InsecurePattern.objects.filter(user=user)
            
        return public_patterns