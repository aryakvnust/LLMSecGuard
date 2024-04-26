from django.contrib import admin
from apps.results.models import Result

# Register your models here.

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('issue_count', 'created_at', 'benchmark', 'model', 'analyzer', 'user')
    search_fields = ('issue_count', 'model__name', 'analyzer__name', 'user__username')
    list_filter = ('benchmark', 'model', 'analyzer', 'user', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'analyzer', 'model')
    list_select_related = ('model', 'analyzer', 'user')
