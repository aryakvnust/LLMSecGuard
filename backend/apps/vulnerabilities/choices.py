from django.db.models import TextChoices

class SeverityChoices(TextChoices):
    LOW = 'l', 'Low'
    MEDIUM = 'm', 'Medium'
    HIGH = 'h', 'High'
    CRITICAL = 'c', 'Critical'