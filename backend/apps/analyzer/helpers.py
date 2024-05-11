from apps.analyzer.models import Analyzer, History, MonthlySumCache
from apps.analyzer.rest.serializers import RuleSerializer
from apps.dispatcher.models import LlmModel

import requests
import datetime

def analyze_code(user, data, model_id):
    analyzers = Analyzer.objects.filter(is_public=True)
    model = LlmModel.objects.get(id=model_id)

    if user.is_authenticated:
        analyzers = analyzers | Analyzer.objects.filter(user=user)

    results = []
    saved = []
    rules = {}
    fix = None

    for analyzer in analyzers:

        for rule in analyzer.rule_set.all():
            rules[rule.id] = rule

        result = requests.post(analyzer.url, json={
            'lang': data['lang'],
            'code': data['code'],
            'rules': [{ 
                'id': rule.id,
                'rule': rule.rule
            } for rule in rules.values()]
        })

        for res in result.json()['results']:
            line = res['line']
            rule = res['rule']

            if (line, rule) in saved:
                continue

            saved.append((line, rule))
            results.append({
                'code': res['code'],
                'line': res['line'],
                'rule': RuleSerializer(rules[res['rule']]).data
            })

            History.objects.create(
                rule=rules[res['rule']],
                model=model
            )

    if len(results) > 0:
        query = f"""
            Fix these vulnerabilities in the following code:\n
        """

        for res in results:
            print("===== RES: ", res)
            query += "- " + res['rule']['name'] + "(" + res['rule']['description'] + ") at line " + str(res['line']) + "\n"

        query += "\n\n    Only return the code, DONT'T include any other information,\n    such as a preamble or suffix.\n"

        fix = model.query(query)
        fix = fix.strip()

    date = datetime.date.today().strftime('%Y-%m')
    cache, _ = MonthlySumCache.objects.get_or_create(date=date, model=model)
    cache.usage += 1
    cache.errors += len(results)
    cache.save()

    return {'results': results, 'fix': fix}

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