from django.contrib import admin
from apps.benchmark_agent.models import Benchmark, MonthlySumCache

# Register your models here.

@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ('model', 'branch', 'metric1', 'metric2', 'metric3', 'metric4', 'metric5', 'created_at')
    list_filter = ('branch', 'model')
    search_fields = ('branch', 'model')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
@admin.register(MonthlySumCache)
class MonthlySumCacheAdmin(admin.ModelAdmin):
    list_display = ('model', 'date', 'usage', 'errors')
    list_filter = ('model', 'date')
    readonly_fields = ('date', 'model', 'usage', 'errors')
    search_fields = ('model', 'date')
    ordering = ('-date',)

