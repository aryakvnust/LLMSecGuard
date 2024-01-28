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

class Engine(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, null=True, blank=True)
    api_type = models.CharField(max_length=100, choices=[(method, method) for method in http_methods])
    api_data = models.CharField(max_length=100, choices=[(body, body) for body in http_body])
    api_params = models.JSONField(max_length=100, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def dispatch(self, language, code):
        dispatcher = None
        headers = {}
        params = self.api_params
        json = None
        data = None
        
        if self.api_key:
            headers['api-key'] = self.api_key
            
            
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
            }
        elif self.api_data == "FORMDATA":
            data = {
                "code": code,
                "language": language
            }
            

        return dispatcher(self.api_url, json=json, data=data, headers=headers, params=params).json()
    
    def __str__(self) -> str:
        return self.name