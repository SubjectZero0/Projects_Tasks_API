# Generated by Django 4.1.4 on 2023-01-02 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_projects_project_prog_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='project_prog_percent',
            field=models.IntegerField(default=0),
        ),
    ]
