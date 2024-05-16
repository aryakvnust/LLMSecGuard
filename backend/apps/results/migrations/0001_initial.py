# Generated by Django 5.0.2 on 2024-05-16 04:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prompt_agent', '0001_initial'),
        ('security_agent', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('benchmark', models.BooleanField(default=False)),
                ('analyzer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='security_agent.analyzer')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prompt_agent.llmmodel')),
                ('rules', models.ManyToManyField(to='security_agent.rule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': 'Results',
                'ordering': ('-created_at',),
            },
        ),
    ]
