from rest_framework import serializers
from .models import LogMaster, ActivityLog

class LogMasterSerializer(serializers.ModelSerializer):
    # Helpful read-only fields to send context to the frontend team
    project_name = serializers.ReadOnlyField(source='project.project_name')
    task_name = serializers.ReadOnlyField(source='task.task_name')
    user_name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = LogMaster
        fields = [
            'id', 'project', 'project_name', 'task', 'task_name', 
            'user', 'user_name', 'log_date', 'total_spent_hrs', 'note'
        ]


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'