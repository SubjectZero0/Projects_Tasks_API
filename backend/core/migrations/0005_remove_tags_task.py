# Generated by Django 4.1.4 on 2023-01-02 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_projects_project_prog_percent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='task',
        ),
    ]
