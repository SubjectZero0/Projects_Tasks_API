"""
Task and Project API Views
"""

from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer, TaskSerializer, TagSerializer
from core.models import Projects, Tasks

# --------------------------------------------------------------------

# Create your views here.


class ProjectAPIViewSet(ModelViewSet):
    """
    API Endpoints for Projects.
    Only Authenticated users have access.
    Authenticated users can only view and handle their own
    Projects.
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['project_title', 'project_descr']

    #           Methods Below
    # -----------------------------------------

    def get_queryset(self):
        """
        The queryset is modified to only look for the projects
        the user has created
        """
        query = Projects.objects.filter(project_owner=self.request.user)
        return query

    def perform_create(self, serializer):
        """
        Creates a project instance with 'project_owner'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """

        instance = serializer.save(project_owner=self.request.user)

        return instance

    def perform_update(self, serializer):
        """
        Updates a project instance with 'project_owner'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """
        instance = serializer.save(project_owner=self.request.user)
        return instance

# --------------------------------------------------------------------


class TaskAPIViewSet(ModelViewSet):
    """
    API Endpoints for Tasks.
    Only Authenticated users have access.
    Authenticated users can only view and handle their own
    Tasks.
    """
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['task_title', 'task_descr', 'task_tags__tag_name']

    #           Methods Below
    # -----------------------------------------

    def get_queryset(self):
        """
        The queryset is modified to only look for the Tasks
        the user has created
        """
        query = Tasks.objects.filter(task_owner=self.request.user)
        return query

    def perform_create(self, serializer):
        """
        Creates a project instance with 'task_owner'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """
        instance = serializer.save(task_owner=self.request.user)
        return instance

    def perform_update(self, serializer):
        """
        Updates a project instance with 'task_owner'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """
        instance = serializer.save(task_owner=self.request.user)
        return instance
