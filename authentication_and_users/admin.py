# from django.contrib import admin
# from .models import *

# admin.site.register(Role)
# admin.site.register(UserMaster)
# admin.site.register(UserSkill)
# admin.site.register(UserMedia)


from django.contrib import admin
from .models import *

# 1. Clear, safe registration format
admin.site.register(Role)
admin.site.register(UserMaster)
admin.site.register(UserSkill)
admin.site.register(UserMedia)


try:
    # Removed 'created_by' columns completely to clear the AttributeError
    admin.site.get_model_admin(UserMaster).list_display = ('id', 'name', 'email', 'department')
    admin.site.get_model_admin(UserMaster).list_filter = ('department',)
    admin.site.get_model_admin(UserMaster).search_fields = ('name', 'email')
    
    # Simple ID lookup tracking column for Roles table view
    admin.site.get_model_admin(Role).list_display = ('id','role_name')

    admin.site.get_model_admin(UserMedia).list_display = ('id', 'user', 'system_path')

    admin.site.get_model_admin(UserSkill).list_display = ('id', 'user', 'skill_name')
    admin.site.get_model_admin(UserSkill).list_filter = ('skill_name',)
except Exception:
    pass