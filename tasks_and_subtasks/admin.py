# from django.contrib import admin
# from .models import TaskListMaster, TaskMaster, SubTaskMaster, TaskAssignee

# admin.site.register(TaskListMaster)
# admin.site.register(TaskMaster)
# admin.site.register(SubTaskMaster)
# admin.site.register(TaskAssignee)


from django.contrib import admin
from .models import TaskListMaster, TaskMaster, SubTaskMaster, TaskAssignee

admin.site.register(TaskListMaster)
admin.site.register(TaskMaster)
admin.site.register(SubTaskMaster)
admin.site.register(TaskAssignee)


try:
    task_list_admin = admin.site.get_model_admin(TaskListMaster)
    task_list_fields = [f.name for f in TaskListMaster._meta.get_fields()]
    
    tl_columns = ['id']
    for f in ['name', 'status']:
        if f in task_list_fields:
            tl_columns.append(f)
    task_list_admin.list_display = tuple(tl_columns)
    
    if 'status' in task_list_fields:
        task_list_admin.list_filter = ('status',)
    if 'name' in task_list_fields:
        task_list_admin.search_fields = ('name',)

    task_admin = admin.site.get_model_admin(TaskMaster)
    task_fields = [f.name for f in TaskMaster._meta.get_fields()]
    
    t_columns = ['id']
    for f in ['name', 'task_list', 'priority', 'status', 'estimated_hrs']:
        if f in task_fields:
            t_columns.append(f)
    task_admin.list_display = tuple(t_columns)
    
    t_filters = []
    for f in ['status', 'priority', 'task_list']:
        if f in task_fields:
            t_filters.append(f)
    if t_filters:
        task_admin.list_filter = tuple(t_filters)
        
    if 'name' in task_fields:
        task_admin.search_fields = ('name',)

    subtask_admin = admin.site.get_model_admin(SubTaskMaster)
    subtask_fields = [f.name for f in SubTaskMaster._meta.get_fields()]
    
    st_columns = ['id']
    name_field = 'sub_task_name' if 'sub_task_name' in subtask_fields else 'name' if 'name' in subtask_fields else None
    if name_field:
        st_columns.append(name_field)
        
    for f in ['parent_task', 'status', 'estimated_hrs']:
        if f in subtask_fields:
            st_columns.append(f)
    subtask_admin.list_display = tuple(st_columns)
    
    st_filters = []
    for f in ['status', 'parent_task']:
        if f in subtask_fields:
            st_filters.append(f)
    if st_filters:
        subtask_admin.list_filter = tuple(st_filters)
        
    if name_field:
        subtask_admin.search_fields = (name_field,)

    assignee_admin = admin.site.get_model_admin(TaskAssignee)
    assignee_fields = [f.name for f in TaskAssignee._meta.get_fields()]
    
    as_columns = ['id']
    for f in ['task', 'user', 'billing_status']:
        if f in assignee_fields:
            as_columns.append(f)
    assignee_admin.list_display = tuple(as_columns)
    
    as_filters = []
    for f in ['billing_status', 'user', 'task']:
        if f in assignee_fields:
            as_filters.append(f)
    if as_filters:
        assignee_admin.list_filter = tuple(as_filters)

except Exception:
    pass