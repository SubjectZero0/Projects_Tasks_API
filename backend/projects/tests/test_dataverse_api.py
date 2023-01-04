"""
Task and Project API tests
"""

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError

from core.models import Projects, Tags, Tasks

# -------------------------------------------------------

TASK_URL = reverse('tasks-list')
PROJ_URL = reverse('projects-list')


def create_superuser(**params):
    """
    Helper function to create superusers
    """
    return get_user_model().objects.create_superuser(**params)

# ----------------------------------------------------------


class TestTaskAPI(APITestCase):
    """
    Tests for the Task API
    """

    def setUp(self):
        """
        Create a user and authenticate them.
        """
        superuser_creds = {
            'email': 'test@test.com',
            'name': 'test',
            'password': 'testpass'
        }

        self.superuser = create_superuser(**superuser_creds)
        self.client.force_authenticate(user=self.superuser)

    def test_get_tasks(self):
        """
        Tests authenticated user can GET their Tasks.
        """
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        """
        Tests if authenticated user can create a task.
        """
        payload = {
            'task_title': 'Test task title',
            'task_descr': 'Test task description',
            'task_prog_percent': 50,
            'task_finish_date': '2023-01-01',
            'task_tags': [{'tag_name': 'test tag name'}]

        }

        res = self.client.post(TASK_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['task_title'], 'Test task title')

    def test_update_task(self):
        """
        Tests if authenticated user can update a task.
        After updating task_prog_percent to 100%,
        checks if  turns to True automatically.

        Then tests if authenticated user can update task proggress.
        """
        # Create a task
        task_details = {
            'task_title': 'Test task title',
            'task_descr': 'Test task description',
            'task_prog_percent': 50,
            'task_finish_date': '2023-01-01',
            'task_tags': [{'tag_name': 'test tag name'}]

        }

        res = self.client.post(TASK_URL, task_details, format='json')
        task = Tasks.objects.get(task_title='Test task title')

        # update a task and make sure task_prog_percent = 100
        payload = {
            'task_title': 'Test task title2',
            'task_descr': 'Test task description2',
            'task_prog_percent': 100,
            'task_finish_date': '2023-01-01',
            'task_tags': [{'tag_name': 'test tag name'}]

        }

        TASK_DETAIL_URL = reverse('tasks-detail', kwargs={'pk': task.id})

        res = self.client.patch(TASK_DETAIL_URL, payload, format='json')

        # confirm update is successful
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # confirm task title is updated.
        self.assertEqual(res.data['task_title'], 'Test task title2')

        # Update task again and attempt to change task_prog_percent =10
        payload = {
            'task_title': 'Test task title3',
            'task_descr': 'Test task description3',
            'task_prog_percent': 10,
            'task_finish_date': '2023-01-01',
            'task_tags': [{'tag_name': 'test tag name'}]
        }

        res = self.client.patch(TASK_DETAIL_URL, payload, format='json')

        completed_task = Tasks.objects.get(task_title='Test task title3')

        # confirm task update is successful
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # confirm task title is updated.
        self.assertEqual(res.data['task_title'], 'Test task title3')

        # confirm task_prog_percent did not change
        self.assertEqual(res.data['task_prog_percent'], 100)

    def test_delete_task(self):
        """
        Test for deleteing a Task.
        """
        # Create a task
        task_details = {
            'task_title': 'Test task title',
            'task_descr': 'Test task description',
            'task_prog_percent': 50,
            'task_finish_date': '2023-01-01',
            'task_tags': [{'tag_name': 'test tag name'}]

        }

        res = self.client.post(TASK_URL, task_details, format='json')
        task = Tasks.objects.get(task_title='Test task title')

        TASK_DETAIL_URL = reverse('tasks-detail', kwargs={'pk': task.id})

        res = self.client.delete(TASK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

# --------------------------------------------------------------------


class TestProjectAPI(APITestCase):
    """
    Tests for the Projects API
    """

    def setUp(self):
        """
        Create a user and authenticate them.
        """
        superuser_creds = {
            'email': 'test@test.com',
            'name': 'test',
            'password': 'testpass'
        }

        self.superuser = create_superuser(**superuser_creds)
        self.client.force_authenticate(user=self.superuser)

    def test_get_projects(self):
        """
        Tests authenticated user can GET their Projects.
        """
        res = self.client.get(PROJ_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        """
        Tests if authenticated user can create a project.
        """
        payload = {
            'project_title': 'TEST TITLE',
            'project_descr': 'TEST DESC',
            'project_finish_date': '2023-01-01',

        }

        res = self.client.post(PROJ_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['project_title'], 'TEST TITLE')

    def test_calc_project_progression(self):
        """
        Test to calculate a projects progression
        as a weighted average of its tasks progression.
        """

        # create a project
        proj_details = {
            'project_title': 'TEST TITLE',
            'project_descr': 'TEST DESC',
            'project_finish_date': '2023-01-01',

        }

        res = self.client.post(PROJ_URL, proj_details, format='json')

        # GET the project's object id to pass in task_details
        project_id = Projects.objects.get(
            project_title='TEST TITLE').project_id

        # Create a task and associate it with the project
        task_details = {
            'task_title': 'Test task title',
            'task_descr': 'Test task description',
            'task_prog_percent': 50,
            'task_finish_date': '2023-01-01',
            'parent_project': project_id,
            'task_owner': self.superuser.id,
            'task_tags': [{'tag_name': 'test tag name'}]

        }

        res = self.client.post(TASK_URL, task_details, format='json')
        task = Tasks.objects.get(task_title='Test task title')

        # Confirm task was created
        self.assertEqual(task.task_title, 'Test task title')
        self.assertEqual(task.task_prog_percent, 50)

        # GET the project detail
        PROJ_DETAIL_URL = reverse('projects-detail', kwargs={'pk': project_id})
        project_res = self.client.get(PROJ_DETAIL_URL)

        # since we only have one task at 50%, project's overall progression should be 50%:
        self.assertEqual(project_res.data['project_prog_percent'], 50)
