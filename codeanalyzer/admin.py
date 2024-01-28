from django.contrib import admin
from .models import Engine, InsecurePattern

# Register your models here.

@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_url')
    
@admin.register(InsecurePattern)
class InsecurePatternAdmin(admin.ModelAdmin):
    list_display = ('cwe_id', 'rule', 'severity', 'analyzer', 'public', 'approved')