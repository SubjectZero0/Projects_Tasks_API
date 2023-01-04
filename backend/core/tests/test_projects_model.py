"""
Tests for Projects Model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Projects


def create_superuser(**params):
    """
    Helper function to create superusers
    """
    return get_user_model().objects.create_superuser(**params)


class TestProjectsModel(TestCase):
    """
    Tests Projects' objects creation.
    """

    def setUp(self):
        superuser_creds = {
            'email': 'test@test.com',
            'name': 'test',
            'password': 'testpass'
        }

        self.superuser = create_superuser(**superuser_creds)

    def test_project_create(self):
        """
        Tests the creation of project, task and tag
        """

        project = {
            'project_title': "Test Project",
            'project_descr': 'Test Description',
            'project_prog_percent': 50,
            'project_finish_date': "2023-01-01",
            'project_owner': self.superuser

        }

        new_project = Projects.objects.create(**project)
        self.assertEqual(new_project.project_title, "Test Project")
