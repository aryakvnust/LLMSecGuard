from django.contrib import admin
from apps.analyzer.models import Analyzer, Rule, Benchmark

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
    
@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ('model', 'branch', 'metric1', 'metric2', 'metric3', 'metric4', 'metric5', 'created_at')
    list_filter = ('branch', 'model')
    search_fields = ('branch', 'model')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
