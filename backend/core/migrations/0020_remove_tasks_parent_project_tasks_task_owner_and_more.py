# Generated by Django 4.1.4 on 2023-01-03 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_tasks_parent_project_tasks_parent_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='parent_project',
        ),
        migrations.AddField(
            model_name='tasks',
            name='task_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='task_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projects',
            name='project_owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='project_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projects',
            name='project_tasks',
            field=models.ManyToManyField(blank=True, to='core.tasks'),
        ),
    ]