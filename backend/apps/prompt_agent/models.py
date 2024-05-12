from django.db import models

from apps.prompt_agent.choices import LlmTypes
from apps.prompt_agent.dispatcher import create

# Create your models here.

class LlmModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    model = models.CharField(max_length=100, choices=[(x, x) for x in LlmTypes])
    api_key = models.CharField(max_length=100, blank=True, null=True)
    
    summary = models.TextField(blank=True, null=True)

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    deleted = models.BooleanField(default=False)
    
    def query(self, prompt):
        provider = create(self.model + "::" + self.api_key)
        response = provider.query(prompt)
        
        LlmResponse.objects.create(
            model=self,
            prompt=prompt,
            response=response
        )
        
        return response
    
    def delete(self):
        self.deleted = True
        self.save()
        
    def __str__(self):
        return self.name
    
class LlmResponse(models.Model):
    model = models.ForeignKey(LlmModel, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.prompt
