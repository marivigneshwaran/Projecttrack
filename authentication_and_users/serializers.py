from rest_framework import serializers
from .models import Role, UserMaster, UserSkill, UserMedia

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserMasterSerializer(serializers.ModelSerializer):
    # This nested serializer shows the role name instead of just an ID
    role_name = serializers.ReadOnlyField(source='role.role_name')

    class Meta:
        model = UserMaster
        fields = ['id', 'name', 'email', 'role', 'role_name', 'designation', 'department']
        extra_kwargs = {'password': {'write_only': True}} # Hide password in JSON output

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'

class UserMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedia
        fields = '__all__'