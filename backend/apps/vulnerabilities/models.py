from django.db import models
from apps.vulnerabilities.choices import SeverityChoices

# Create your models here.

class Vulnerability(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    severity = models.CharField(max_length=1, choices=SeverityChoices.choices, default=SeverityChoices.LOW)
    
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Vulnerability'
        verbose_name_plural = 'Vulnerabilities'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
