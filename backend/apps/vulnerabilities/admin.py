from django.contrib import admin
from apps.vulnerabilities.models import Vulnerability

# Register your models here.
@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'is_approved', 'is_public', 'created_at')
    list_filter = ('severity', 'is_approved', 'is_public')
    search_fields = ('name', 'severity', 'is_approved', 'is_public')
    ordering = ('-created_at',)
