from apps.benchmark_agent.models import MonthlySumCache
from apps.prompt_agent.models import LlmModel

import requests
import datetime

def get_top_model():
    # Get the current month and year
    date = datetime.date.today().strftime('%Y-%m')

    # Get the models with the most usage for the current month
    top_models = MonthlySumCache.objects.filter(date=date).order_by('-usage')[:5]

    # Sort the top models by the least amount of errors
    top_models = sorted(top_models, key=lambda x: x.errors)
    
    if len(top_models) == 0:
        return LlmModel.objects.all().order_by('-id').first()

    return top_models[0].model