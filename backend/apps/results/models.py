from django.db import models

# Create your models here.

class Result(models.Model):
    issue_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    benchmark = models.BooleanField(default=False)
    
    model = models.ForeignKey("dispatcher.LlmModel", on_delete=models.CASCADE)
    analyzer = models.ForeignKey("analyzer.Analyzer", on_delete=models.CASCADE)
    rules = models.ManyToManyField("analyzer.Rule")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
        ordering = ('-created_at',)
