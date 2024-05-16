from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.security_agent.models import Benchmark
from apps.security_agent.choices import BenchmarkTypeChoices
from apps.prompt_agent.models import LlmModel
from json import loads

class Command(BaseCommand):
    help = 'Import Results from PurpleLlama Benchmark'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='path of the instruct.json')
        
    def handle(self, *args, **options):
        path = options['path']
        
        with open(path, 'r', encoding="UTF-8") as file:
            data = file.read()
            data = loads(data)
            
            stat_per_model = data.get('stat_per_model')
            stat_per_model_per_variant = data.get('stat_per_model_per_variant')
            stat_per_model_per_type = data.get('stat_per_model_per_type')
            stat_per_model_per_risk_category = data.get('stat_per_model_per_risk_category')
            
            accept_count = data.get('accept_count')
            refusal_count = data.get('refusal_count')
            refusal_rate = data.get('refusal_rate')
            
            if stat_per_model is not None:
                del data['stat_per_model']
                
                for model, stat in stat_per_model.items():
                    models = LlmModel.objects.filter(model__endswith=model)
                    
                    for model in models:
                        Benchmark.objects.create(
                            branch=BenchmarkTypeChoices.STATS_PER_MODEL,
                            model=model,
                            metric1=stat['injection_successful_count'],
                            metric2=stat['injection_unsuccessful_count'],
                            metric3=stat['total_count'],
                            metric4=stat['injection_successful_percentage'],
                            metric5=stat['injection_unsuccessful_percentage']
                        )
                        
                        self.stdout.write(self.style.SUCCESS(f"SP: Created for model {model}"))
                
            # IR, IP
            if stat_per_model_per_variant is not None:
                del data['stat_per_model_per_variant']
                
                for model, stat in stat_per_model_per_variant.items():
                    models = LlmModel.objects.filter(model__endswith=model)
                    
                    for model in models:
                        Benchmark.objects.create(
                            branch=BenchmarkTypeChoices.IGNORE_PREVIOUS_INSTRUCTIONS,
                            model=model,
                            metric1=stat['ignore_previous_instructions']['injection_successful_count'],
                            metric2=stat['ignore_previous_instructions']['injection_unsuccessful_count'],
                            metric3=stat['ignore_previous_instructions']['total_count'],
                            metric4=stat['ignore_previous_instructions']['injection_successful_percentage'],
                            metric5=stat['ignore_previous_instructions']['injection_unsuccessful_percentage']
                        )
                        self.stdout.write(self.style.SUCCESS(f"IP: Created for model {model}"))
                        
                        Benchmark.objects.create(
                            branch=BenchmarkTypeChoices.INDIRECT_REFERENCE,
                            model=model,
                            metric1=stat['indirect_reference']['injection_successful_count'],
                            metric2=stat['indirect_reference']['injection_unsuccessful_count'],
                            metric3=stat['indirect_reference']['total_count'],
                            metric4=stat['indirect_reference']['injection_successful_percentage'],
                            metric5=stat['indirect_reference']['injection_unsuccessful_percentage']
                        )
                        
                        self.stdout.write(self.style.SUCCESS(f"IR: Created for model {model}"))
                
            # DR
            if stat_per_model_per_type is not None:
                del data['stat_per_model_per_type']
                
                for model, stat in stat_per_model_per_type.items():
                    models = LlmModel.objects.filter(model__endswith=model)
                    
                    for model in models:
                        Benchmark.objects.create(
                            branch=BenchmarkTypeChoices.DIRECT,
                            model=model,
                            metric1=stat['direct']['injection_successful_count'],
                            metric2=stat['direct']['injection_unsuccessful_count'],
                            metric3=stat['direct']['total_count'],
                            metric4=stat['direct']['injection_successful_percentage'],
                            metric5=stat['direct']['injection_unsuccessful_percentage']
                        )
                        
                        self.stdout.write(self.style.SUCCESS(f"DR: Created for model {model}"))
             
            # SV
            if stat_per_model_per_risk_category is not None:
                del data['stat_per_model_per_risk_category']
                
                for model, stat in stat_per_model_per_risk_category.items():
                    models = LlmModel.objects.filter(model__endswith=model)
                    
                    for model in models:
                        Benchmark.objects.create(
                            branch=BenchmarkTypeChoices.DIRECT,
                            model=model,
                            metric1=stat['security-violating']['injection_successful_count'],
                            metric2=stat['security-violating']['injection_unsuccessful_count'],
                            metric3=stat['security-violating']['total_count'],
                            metric4=stat['security-violating']['injection_successful_percentage'],
                            metric5=stat['security-violating']['injection_unsuccessful_percentage']
                        )
                        
                        self.stdout.write(self.style.SUCCESS(f"SV: Created for model {model}"))
                
            if accept_count is not None:
                del data['accept_count']        
                
            if refusal_count is not None:
                del data['refusal_count']
                
            if refusal_rate is not None:
                del data['refusal_rate']
                
            # PE
            for model, stat in data.items():
                data = stat.get('Privilege Escalation')
                if data is None:
                    continue
            
                models = LlmModel.objects.filter(model__endswith=model)
                for model in models:
                    Benchmark.objects.create(
                        branch=BenchmarkTypeChoices.PRIVILEGE_ESCALATION,
                        model=model,
                        metric1=data['is_extremely_malicious'],
                        metric2=data['is_potentially_malicious'],
                        metric3=data['is_non_malicious'],
                        metric4=data['total_count'],
                        metric5=data['malicious_percentage']
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f"PE: Created for model {model}"))
        