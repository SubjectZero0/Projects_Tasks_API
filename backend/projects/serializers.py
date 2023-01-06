"""
Serializers for Projects, Tasks and Tags.
"""

import math
from rest_framework import serializers

from django.contrib.auth import get_user_model

from core.models import Projects, Tasks, Tags

# ----------------------------------------------------


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tags.
    """
    class Meta:
        model = Tags
        fields = ['tag_name']

# ----------------------------------------------------------


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Projects' Tasks.
    Supports creation and update of nested tags.

    """
    task_tags = TagSerializer(many=True, required=False)
    task_prog_percent = serializers.IntegerField(min_value=0, max_value=100)

    class Meta:
        model = Tasks
        fields = '__all__'
        read_only_fields = ['id', 'task_owner']

    #               Methods Below
    # ---------------------------------------------

    def _get_or_create_tags(self, tags, task):
        """
        Helper function to ADD task_tags
        """
        for tag in tags:
            tag_obj, created = Tags.objects.get_or_create(**tag)
            task.task_tags.add(tag_obj)

    def create(self, validated_data):
        """
        Handle creation of task and nested tags
        """
        tags = validated_data.pop('task_tags', [])
        task = Tasks.objects.create(**validated_data)

        self._get_or_create_tags(tags, task)
        return task

    def update(self, instance, validated_data):
        """
        Handle update of task and nested tags.

        If task_prog_percent was already 100,
        on update, the new value gets removed and 
        replaced with 100. Effectively making the field
        not editable.
        """
        tags = validated_data.pop('task_tags', None)

        if instance.task_prog_percent >= 100:
            validated_data.pop('task_prog_percent')
            instance.task_prog_percent = 100

        if tags is not None:
            """
            if tags exist, clears them.
            Calls helper function to create tags and ADD them to instance
            """
            instance.task_tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance
# ----------------------------------------------------------


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Projects. Authenticated users can see 
    their projects only.

    Automatically calculates project progression by the 
    progression of the tasks associated with it.
    """
    project_prog_percent = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = '__all__'
        read_only_fields = ['project_id', 'project_owner']

    #               Methods Below
    # ---------------------------------------------

    def get_project_prog_percent(self, obj):
        """
        Method to calculate the average
        of project's tasks progression.
        """
        tasks = Tasks.objects.filter(parent_project=obj)
        sum = 0

        try:
            for task in tasks:
                sum += task.task_prog_percent

            obj.project_prog_percent = math.floor(sum/len(tasks))

        except:
            obj.project_prog_percent = 0

        return obj.project_prog_percent
