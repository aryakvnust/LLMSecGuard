from apps.security_agent.models import Analyzer
from apps.benchmark_agent.models import History, MonthlySumCache
from apps.security_agent.rest.serializers import RuleSerializer
from apps.prompt_agent.models import LlmModel

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
