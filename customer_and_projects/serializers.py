from rest_framework import serializers
from .models import CustomerMaster, ProjectMaster, PhaseMaster

class CustomerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMaster
        fields = '__all__'


class ProjectMasterSerializer(serializers.ModelSerializer):
    # This read-only field displays the customer's name directly in the project JSON payload
    client_name = serializers.ReadOnlyField(source='client.name')

    class Meta:
        model = ProjectMaster
        fields = [
            'id', 'project_name', 'client', 'client_name', 
            'project_type', 'start_date', 'due_date', 
            'status', 'progress_percent'
        ]


class PhaseMasterSerializer(serializers.ModelSerializer):
    # Displays the parent project's name directly inside the phase data breakdown
    project_name = serializers.ReadOnlyField(source='project.project_name')

    class Meta:
        model = PhaseMaster
        fields = [
            'id', 'phase_name', 'project', 'project_name', 
            'budget', 'start_date', 'due_date', 'status'
        ]