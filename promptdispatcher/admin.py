from django.contrib import admin
from .models import LLM, Results

# Register your models here.

@admin.register(LLM)
class LLMAdmin(admin.ModelAdmin):
    list_display = ('model', 'api_key')
    
    
@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ('model', 'issue_count', 'created_at')