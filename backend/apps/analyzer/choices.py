from django.db.models import TextChoices

class LanguageChoices(TextChoices):
    PYTHON = 'PY', 'Python'
    JAVASCRIPT = 'JS', 'JavaScript'
    JAVA = 'JV', 'Java'
    RUBY = 'RB', 'Ruby'
    PHP = 'PH', 'PHP'
    GO = 'GO', 'Go'
    C = 'C', 'C'
    CPP = 'CP', 'C++'
    CSHARP = 'C#', 'C#'
    TYPESCRIPT = 'TS', 'TypeScript'
    SWIFT = 'SW', 'Swift'
    KOTLIN = 'KT', 'Kotlin'
    SCALA = 'SC', 'Scala'
    RUST = 'RS', 'Rust'
    SHELL = 'SH', 'Shell'
    OBJECTIVEC = 'OC', 'Objective-C'
    BASH = 'BS', 'Bash'
    SQL = 'SQ', 'SQL'
    HTML = 'HT', 'HTML'
    CSS = 'CS', 'CSS'
    OTHER = 'OT', 'Other'
    
class BenchmarkTypeChoices(TextChoices):
    STATS_PER_MODEL = 'SM', 'Stats per Model'
    
    INDIRECT_REFERENCE = 'IR', 'Indirect Reference'
    IGNORE_PREVIOUS_INSTRUCTIONS = 'IP', 'Ignore Previous Instructions'
    DIRECT = 'DR', 'Direct'
    SECURITY_VIOLATING = 'SV', 'Security Violating'
    PRIVILEGE_ESCALATION = 'PE', 'Privilege Escalation'