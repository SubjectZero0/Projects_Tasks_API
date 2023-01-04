"""
Tests for Tasks Model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tasks, Tags


def create_superuser(**params):
    """
    Helper function to create superusers
    """
    return get_user_model().objects.create_superuser(**params)


class TestTasksModel(TestCase):
    """
    Tests Tasks' object creation.
    """

    def setUp(self):
        superuser_creds = {
            'email': 'test@test.com',
            'name': 'test',
            'password': 'testpass'
        }

        self.superuser = create_superuser(**superuser_creds)

    def test_task_create(self):
        """
        Tests creation on Tasks Model object.
        """
        task = {
            'task_title': 'test task',
            'task_descr': 'test task descr',
            'task_prog_percent': 10,
            'task_finish_date': "2023-01-01",
            'task_owner': self.superuser
        }
        new_task = Tasks.objects.create(**task)
        self.assertEqual(new_task.task_title, "test task")
        tag = {
            'tag_name': 'test tag'
        }
        new_tag = Tags.objects.create(**tag)
        self.assertEqual(new_tag.tag_name, "test tag")
