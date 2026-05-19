# from django.contrib import admin
# from .models import *

# admin.site.register(CustomerMaster)
# admin.site.register(ProjectMaster)
# admin.site.register(PhaseMaster)

# try:
#     # Removed 'created_by' columns completely to clear the AttributeError
#     admin.site.get_model_admin(CustomerMaster).list_display = ('id', 'name', 'email', 'phone', 'active_status')
#     admin.site.get_model_admin(CustomerMaster).list_filter = ('active_status',)
#     admin.site.get_model_admin(CustomerMaster).search_fields = ('name', 'email')
    
#     # Simple ID lookup tracking column for Roles table view
#     admin.site.get_model_admin(ProjectMaster).list_display = ('id','project_name', 'client', 'start_date', 'due_date', 'status')
#     admin.site.get_model_admin(CustomerMaster).list_filter = ('status', 'client', )
#     admin.site.get_model_admin(CustomerMaster).search_fields = ('project_name', 'client')

#     admin.site.get_model_admin(PhaseMaster).list_display = ('id', 'project', 'phase_name', 'start_date', 'due_date', 'status')
#     admin.site.get_model_admin(CustomerMaster).list_filter = ('project', 'status', )
#     admin.site.get_model_admin(CustomerMaster).search_fields = ('project', 'phase_name')

# except Exception:
#     pass


from django.contrib import admin
from .models import CustomerMaster, ProjectMaster, PhaseMaster

admin.site.register(CustomerMaster)
admin.site.register(ProjectMaster)
admin.site.register(PhaseMaster)


try:
    customer_admin = admin.site.get_model_admin(CustomerMaster)
    customer_fields = [f.name for f in CustomerMaster._meta.get_fields() if not f.many_to_many and not f.one_to_many]
    
    chosen_customer_columns = ['id']
    
    possible_desc_fields = ['customer_name', 'name', 'company_name', 'company', 'email', 'phone', 'mobile']
    added_count = 0
    for field in possible_desc_fields:
        if field in customer_fields and added_count < 3:
            chosen_customer_columns.append(field)
            added_count += 1
            
    if 'active_status' in customer_fields:
        chosen_customer_columns.append('active_status')
    elif 'status' in customer_fields:
        chosen_customer_columns.append('status')
        
    if len(chosen_customer_columns) == 1:
        chosen_customer_columns.append('__str__')
        
    customer_admin.list_display = tuple(chosen_customer_columns)
    
    if 'active_status' in customer_fields:
        customer_admin.list_filter = ('active_status',)
    elif 'status' in customer_fields:
        customer_admin.list_filter = ('status',)
        
    for search_cand in ['customer_name', 'name', 'company_name', 'email']:
        if search_cand in customer_fields:
            customer_admin.search_fields = (search_cand,)
            break

    project_admin = admin.site.get_model_admin(ProjectMaster)
    project_admin.list_display = ('id', 'project_name', 'project_type', 'status', 'progress_percent')
    project_admin.list_filter = ('status', 'project_type')
    project_admin.search_fields = ('project_name',)

    phase_admin = admin.site.get_model_admin(PhaseMaster)
    phase_admin.list_display = ('id', 'project', 'phase_name', 'status')
    phase_admin.list_filter = ('project', 'status')
    phase_admin.search_fields = ('phase_name',)

except Exception:
    pass