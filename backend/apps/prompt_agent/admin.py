from django.contrib import admin
from apps.prompt_agent.models import LlmModel, LlmResponse

# Register your models here.

@admin.register(LlmModel)
class LlmModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('user', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('user',)
    
@admin.register(LlmResponse)
class LlmResponse(admin.ModelAdmin):
    list_display = ('model', 'prompt', 'created_at')
    search_fields = ('model__name', 'prompt')
    list_filter = ('model', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
