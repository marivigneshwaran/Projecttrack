# from django.contrib import admin
# from .models import LogMaster, ActivityLog

# admin.site.register(LogMaster)
# admin.site.register(ActivityLog)



from django.contrib import admin
from .models import LogMaster, ActivityLog

admin.site.register(LogMaster)
admin.site.register(ActivityLog)


try:
    log_admin = admin.site.get_model_admin(LogMaster)
    log_fields = [f.name for f in LogMaster._meta.get_fields()]
    
    chosen_log_columns = ['id']
    for f in ['project', 'task', 'user', 'log_date', 'total_spent_hrs']:
        if f in log_fields:
            chosen_log_columns.append(f)
            
    log_admin.list_display = tuple(chosen_log_columns)
    
    chosen_log_filters = []
    for f in ['project', 'user', 'log_date']:
        if f in log_fields:
            chosen_log_filters.append(f)
    if chosen_log_filters:
        log_admin.list_filter = tuple(chosen_log_filters)

    activity_admin = admin.site.get_model_admin(ActivityLog)
    activity_fields = [f.name for f in ActivityLog._meta.get_fields()]
    
    chosen_act_columns = ['id']
    for f in ['action', 'activity_type', 'timestamp']:
        if f in activity_fields:
            chosen_act_columns.append(f)
            
    activity_admin.list_display = tuple(chosen_act_columns)
    
    if 'activity_type' in activity_fields:
        activity_admin.list_filter = ('activity_type',)
    elif 'type' in activity_fields:
        activity_admin.list_filter = ('type',)

except Exception:
    pass