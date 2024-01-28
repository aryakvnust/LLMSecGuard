from django.contrib import admin
from .models import Engine

# Register your models here.

@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_url')