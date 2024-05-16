from django.db.models import TextChoices

class BenchmarkTypeChoices(TextChoices):
    STATS_PER_MODEL = 'SM', 'Stats per Model'
    
    INDIRECT_REFERENCE = 'IR', 'Indirect Reference'
    IGNORE_PREVIOUS_INSTRUCTIONS = 'IP', 'Ignore Previous Instructions'
    DIRECT = 'DR', 'Direct'
    SECURITY_VIOLATING = 'SV', 'Security Violating'
    PRIVILEGE_ESCALATION = 'PE', 'Privilege Escalation'