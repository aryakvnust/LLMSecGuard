from django.contrib import admin
from apps.security_agent.models import Analyzer, Rule

# Register your models here.
@admin.register(Analyzer)
class AnalyzerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_approved', 'is_public', 'created_at')
    list_filter = ('is_approved', 'is_public')
    search_fields = ('name', 'is_approved', 'is_public')
    ordering = ('-created_at',)
    
@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'analyzer', 'vulnerability', 'created_at')
    list_filter = ('analyzer', 'vulnerability')
    search_fields = ('name', 'analyzer', 'vulnerability')
    ordering = ('-created_at',)