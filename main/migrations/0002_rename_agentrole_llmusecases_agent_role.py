# Generated by Django 5.1.1 on 2024-09-21 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='llmusecases',
            old_name='agentRole',
            new_name='agent_role',
        ),
    ]
