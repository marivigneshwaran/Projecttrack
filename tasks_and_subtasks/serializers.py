from rest_framework import serializers
from .models import TaskListMaster, TaskMaster, SubTaskMaster, TaskAssignee

class TaskListMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskListMaster
        fields = '__all__'


class TaskMasterSerializer(serializers.ModelSerializer):
    task_list_name = serializers.ReadOnlyField(source='task_list.name')

    class Meta:
        model = TaskMaster
        fields = [
            'id', 'task_name', 'task_list', 'task_list_name', 
            'priority', 'status', 'estimated_hrs'
        ]


class SubTaskMasterSerializer(serializers.ModelSerializer):
    parent_task_name = serializers.ReadOnlyField(source='parent_task.task_name')

    class Meta:
        model = SubTaskMaster
        fields = [
            'id', 'sub_task_name', 'parent_task', 'parent_task_name', 
            'status', 'estimated_hrs'
        ]


class TaskAssigneeSerializer(serializers.ModelSerializer):
    task_name = serializers.ReadOnlyField(source='task.task_name')
    user_name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = TaskAssignee
        fields = [
            'id', 'task', 'task_name', 'user', 'user_name', 'billing_status'
        ]