from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.security_agent.models import Analyzer
from apps.vulnerabilities.models import Vulnerability
from json import loads

class Command(BaseCommand):
    help = 'Import rules from PurpleLlama instruct.json'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the analyzer')
        parser.add_argument('id', type=str, help='id of the analyzer')
        parser.add_argument('path', type=str, help='path of the instruct.json')
        
    def handle(self, *args, **options):
        name = options['name']
        id = options['id']
        path = options['path']
        
        analyzer = Analyzer.objects.get(id=id)
        
        with open(path, 'r', encoding="UTF-8") as file:
            data = file.read()
            data = loads(data)
            
            User = get_user_model()
            admin = User.objects.filter(is_superuser=True).first()
            
            for rule in data:
                if not rule['rule']:
                    continue
                
                if rule['analyzer'] != name:
                    continue
                
                v, c = Vulnerability.objects.get_or_create(
                    name=rule['cwe_identifier'],
                    description=rule['pattern_desc'],
                    user=admin,
                    is_approved=True,
                )
                
                r, c = analyzer.rule_set.get_or_create(
                    name=rule['cwe_identifier'],
                    description=rule['pattern_desc'],
                    rule=rule['rule'],
                    language=rule['language'],
                    vulnerability=v,
                    meta_data={
                        'repo': rule['repo']
                    },
                )
                
                self.stdout.write(self.style.SUCCESS(f"Rule {r.id}<{v.id}> created for analyzer {analyzer.id}"))
                
            
        
        # analyzers = Analyzer.objects.filter(is_public=True)
        # for analyzer in analyzers:
        #     self.stdout.write(self.style.SUCCESS(f'ID: {analyzer.id}, Name: {analyzer.name}'))