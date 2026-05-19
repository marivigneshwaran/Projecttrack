# def get_dashboard_context(request=None):
#     # Base lookups initialization
#     project_filter = request.GET.get('project_filter') if request else None
#     user_filter = request.GET.get('user_filter') if request else None
#     date_filter = request.GET.get('date_filter', '6m') if request else '6m'

#     projects_qs = ProjectMaster.objects.all()
#     tasks_qs = TaskMaster.objects.all()
#     logs_qs = LogMaster.objects.all()
#     activities_qs = ActivityLog.objects.all()

#     # Time-window calculation
#     now = timezone.now()
#     if date_filter == '30d':
#         start_date = now - timedelta(days=30)
#     elif date_filter == '3m':
#         start_date = now - timedelta(days=90)
#     else:
#         start_date = now - timedelta(days=180)

#     # Apply global filter engines
#     if project_filter:
#         projects_qs = projects_qs.filter(id=project_filter)
#         project_task_ids = LogMaster.objects.filter(project_id=project_filter).exclude(task__isnull=True).values_list('task_id', flat=True).distinct()
#         tasks_qs = tasks_qs.filter(id__in=project_task_ids) if project_task_ids.exists() else tasks_qs.filter(task_list__project_id=project_filter) if hasattr(TaskMaster, 'task_list') else tasks_qs.all()
#         logs_qs = logs_qs.filter(project_id=project_filter)
        
#     if user_filter:
#         tasks_qs = tasks_qs.filter(assignees__user_id=user_filter).distinct() if hasattr(TaskMaster, 'assignees') else tasks_qs.all()
#         logs_qs = logs_qs.filter(user_id=user_filter)

#     # Bound trend metrics by date filter selection
#     logs_qs = logs_qs.filter(log_date__gte=start_date.date())

#     log_hours = logs_qs.aggregate(total=Sum('total_spent_hrs'), avg=Avg('total_spent_hrs'))
#     total_projects = projects_qs.count()
#     completed_projects = projects_qs.filter(status='completed').count()

#     totals = {
#         'projects': total_projects,
#         'project_completion_rate': round((completed_projects / total_projects * 100), 1) if total_projects else 0,
#         'tasks': tasks_qs.count(),
#         'task_completion_rate': round((tasks_qs.filter(status='completed').count() / tasks_qs.count() * 100), 1) if tasks_qs.exists() else 0,
#         'subtasks': SubTaskMaster.objects.filter(parent_task__in=tasks_qs).count() if hasattr(SubTaskMaster, 'parent_task') else 0,
#         'customers': CustomerMaster.objects.count(),
#         'customer_active_rate': round((CustomerMaster.objects.filter(active_status='active').count() / CustomerMaster.objects.count() * 100), 1) if CustomerMaster.objects.exists() else 0,
#         'hours_logged': float(log_hours['total'] or 0),
#         'avg_hours_per_log': round(float(log_hours['avg'] or 0), 1),
#         'avg_project_progress': round(float(projects_qs.aggregate(avg=Avg('progress_percent'))['avg'] or 0), 1) if projects_qs.exists() else 0,
#         'phases': PhaseMaster.objects.count(),
#         'time_logs': logs_qs.count(),
#         'assignments': TaskAssignee.objects.count(),
#     }

#     # Core Charts Data Payload Engine
#     # Build both viewpoints for the Project Chart
#     project_status_data = _status_breakdown(projects_qs, field='status')
    
#     pt_rows = projects_qs.values('project_type').annotate(count=Count('pk'))
#     project_type_data = _chart_payload([str(r['project_type']).title() for r in pt_rows], [r['count'] for r in pt_rows], colors=['#6366f1', '#10b981'])

#     charts = {
#         'project_status': project_status_data,
#         'project_type': project_type_data, # Loaded dynamically in frontend toggle
#         'task_status': _status_breakdown(tasks_qs),
#         'task_priority': _status_breakdown(tasks_qs, field='priority'),
#         'billing_status': _status_breakdown(TaskAssignee.objects.filter(task__in=tasks_qs), field='billing_status') if 'tasks_and_subtasks' in request.path or True else _status_breakdown(TaskAssignee.objects.all()),
#     }

#     # Line Chart history data parsing
#     # monthly_logs = logs_qs.annotate(month=TruncMonth('log_date')).values('month').annotate(hours=Sum('total_spent_hrs')).order_by('month')
#     # charts['monthly_hours'] = _chart_payload(
#     #     [row['month'].strftime('%b %Y') if row['month'] else 'N/A' for row in monthly_logs],
#     #     [float(row['hours'] or 0) for row in monthly_logs],
#     #     ['#4f46e5']
#     # )
#     # 1. Base Overall Timeline (Current View)
#     monthly_logs = logs_qs.annotate(month=TruncMonth('log_date')).values('month').annotate(hours=Sum('total_spent_hrs')).order_by('month')
#     months_labels = [row['month'].strftime('%b %Y') if row['month'] else 'N/A' for row in monthly_logs]
    
#     charts['monthly_hours'] = _chart_payload(
#         months_labels,
#         [float(row['hours'] or 0) for row in monthly_logs],
#         ['#4f46e5']
#     )

#     # 2. Advanced Multi-Line Breakdown: Grouped by Project Hierarchy
#     proj_trend_rows = logs_qs.annotate(month=TruncMonth('log_date'))\
#                              .values('month', 'project__project_name')\
#                              .annotate(hours=Sum('total_spent_hrs'))\
#                              .order_by('month')
                             
#     # Structure data payload for unique project arrays
#     unique_projects = list(set(r['project__project_name'] for r in proj_trend_rows if r['project__project_name']))
#     project_datasets = {p: [0.0] * len(months_labels) for p in unique_projects}
    
#     for row in proj_trend_rows:
#         if row['month'] and row['project__project_name']:
#             m_str = row['month'].strftime('%b %Y')
#             if m_str in months_labels:
#                 idx = months_labels.index(m_str)
#                 project_datasets[row['project__project_name']][idx] = float(row['hours'] or 0)

#     charts['timeline_by_project'] = {
#         'labels': months_labels,
#         'datasets': [{'label': name, 'data': data} for name, data in project_datasets.items()]
#     }

#     # 3. Advanced Multi-Line Breakdown: Grouped by Operator/User Hierarchy
#     user_trend_rows = logs_qs.annotate(month=TruncMonth('log_date'))\
#                              .values('month', 'user__name')\
#                              .annotate(hours=Sum('total_spent_hrs'))\
#                              .order_by('month')
                             
#     unique_users = list(set(r['user__name'] for r in user_trend_rows if r['user__name']))
#     user_datasets = {u: [0.0] * len(months_labels) for u in unique_users}
    
#     for row in user_trend_rows:
#         if row['month'] and row['user__name']:
#             m_str = row['month'].strftime('%b %Y')
#             if m_str in months_labels:
#                 idx = months_labels.index(m_str)
#                 user_datasets[row['user__name']][idx] = float(row['hours'] or 0)

#     charts['timeline_by_user'] = {
#         'labels': months_labels,
#         'datasets': [{'label': name, 'data': data} for name, data in user_datasets.items()]
#     }

#     # Dropdowns structuring arrays
#     filter_options = {
#         'projects': list(ProjectMaster.objects.values('id', 'project_name')),
#         'users': list(UserMaster.objects.values('id', 'name')),
#         'selected_project': project_filter,
#         'selected_user': user_filter,
#         'selected_date': date_filter,
#     }

#     recent_activities = list(activities_qs.order_by('-timestamp')[:8].values('action', 'activity_type', 'timestamp'))
#     for item in recent_activities:
#         item['timestamp'] = timezone.localtime(item['timestamp']).strftime('%d %b %Y, %H:%M')

#     recent_logs = list(logs_qs.select_related('project', 'user').order_by('-log_date')[:8].values('log_date', 'total_spent_hrs', 'project__project_name', 'user__name'))
#     for item in recent_logs:
#         item['log_date'] = item['log_date'].strftime('%d %b %Y')
#         item['total_spent_hrs'] = float(item['total_spent_hrs'])

#     return {
#         'dashboard_totals': totals,
#         'dashboard_charts': charts,
#         'dashboard_recent_activities': recent_activities,
#         'dashboard_recent_logs': recent_logs,
#         'filter_options': filter_options,
#     }


from datetime import timedelta
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from authentication_and_users.models import UserMaster, Role, UserSkill
from customer_and_projects.models import CustomerMaster, ProjectMaster, PhaseMaster
from logging_and_activities.models import LogMaster, ActivityLog
from tasks_and_subtasks.models import TaskMaster, SubTaskMaster, TaskAssignee


def _chart_payload(labels, values, colors=None):
    default_colors = [
        '#4f46e5', '#0ea5e9', '#10b981', '#f59e0b',
        '#ef4444', '#8b5cf6', '#ec4899', '#64748b',
    ]
    return {
        'labels': labels,
        'data': values,
        'colors': colors or default_colors[: len(labels)],
    }


def _status_breakdown(queryset, field='status'):
    rows = (
        queryset.values(field)
        .annotate(count=Count('pk'))
        .order_by('-count')
    )
    labels, values = [], []
    for row in rows:
        raw = row[field] or 'unknown'
        labels.append(str(raw).replace('_', ' ').title())
        values.append(row['count'])
    return _chart_payload(labels, values)


def get_dashboard_context(request=None):
    # Base lookups initialization
    project_filter = request.GET.get('project_filter') if request else None
    user_filter = request.GET.get('user_filter') if request else None
    date_filter = request.GET.get('date_filter', '6m') if request else '6m'

    projects_qs = ProjectMaster.objects.all()
    tasks_qs = TaskMaster.objects.all()
    logs_qs = LogMaster.objects.all()
    activities_qs = ActivityLog.objects.all()

    # Time-window calculation
    now = timezone.now()
    if date_filter == '30d':
        start_date = now - timedelta(days=30)
    elif date_filter == '3m':
        start_date = now - timedelta(days=90)
    else:
        start_date = now - timedelta(days=180)

    # Apply global filter engines
    if project_filter:
        projects_qs = projects_qs.filter(id=project_filter)
        project_task_ids = LogMaster.objects.filter(project_id=project_filter).exclude(task__isnull=True).values_list('task_id', flat=True).distinct()
        tasks_qs = tasks_qs.filter(id__in=project_task_ids) if project_task_ids.exists() else tasks_qs.filter(task_list__project_id=project_filter) if hasattr(TaskMaster, 'task_list') else tasks_qs.all()
        logs_qs = logs_qs.filter(project_id=project_filter)
        
    if user_filter:
        tasks_qs = tasks_qs.filter(assignees__user_id=user_filter).distinct() if hasattr(TaskMaster, 'assignees') else tasks_qs.all()
        logs_qs = logs_qs.filter(user_id=user_filter)

    # Bound trend metrics by date filter selection
    logs_qs = logs_qs.filter(log_date__gte=start_date.date())

    log_hours = logs_qs.aggregate(total=Sum('total_spent_hrs'), avg=Avg('total_spent_hrs'))
    total_projects = projects_qs.count()
    completed_projects = projects_qs.filter(status='completed').count()

    totals = {
        'projects': total_projects,
        'project_completion_rate': round((completed_projects / total_projects * 100), 1) if total_projects else 0,
        'tasks': tasks_qs.count(),
        'task_completion_rate': round((tasks_qs.filter(status='completed').count() / tasks_qs.count() * 100), 1) if tasks_qs.exists() else 0,
        'subtasks': SubTaskMaster.objects.filter(parent_task__in=tasks_qs).count() if hasattr(SubTaskMaster, 'parent_task') else 0,
        'customers': CustomerMaster.objects.count(),
        'customer_active_rate': round((CustomerMaster.objects.filter(active_status='active').count() / CustomerMaster.objects.count() * 100), 1) if CustomerMaster.objects.exists() else 0,
        'hours_logged': float(log_hours['total'] or 0),
        'avg_hours_per_log': round(float(log_hours['avg'] or 0), 1),
        'avg_project_progress': round(float(projects_qs.aggregate(avg=Avg('progress_percent'))['avg'] or 0), 1) if projects_qs.exists() else 0,
        'phases': PhaseMaster.objects.count(),
        'time_logs': logs_qs.count(),
        'assignments': TaskAssignee.objects.count(),
    }

    # Core Charts Data Payload Engine
    # Build both viewpoints for the Project Chart
    project_status_data = _status_breakdown(projects_qs, field='status')
    
    pt_rows = projects_qs.values('project_type').annotate(count=Count('pk'))
    project_type_data = _chart_payload([str(r['project_type']).title() for r in pt_rows], [r['count'] for r in pt_rows], colors=['#6366f1', '#10b981'])

    # Groups timesheet entries by task name and sums the total hours spent on each for the toggle filter
    task_time_rows = logs_qs.values('task__task_name')\
                            .annotate(hours=Sum('total_spent_hrs'))\
                            .order_by('-hours')[:6]
    
    task_time_consume_data = _chart_payload(
        [str(r['task__task_name']).title() for r in task_time_rows if r['task__task_name']],
        [float(r['hours'] or 0) for r in task_time_rows if r['task__task_name']]
    )

    charts = {
        'project_status': project_status_data,
        'project_type': project_type_data, 
        'task_status': _status_breakdown(tasks_qs),
        'task_time_consume': task_time_consume_data,
    }

    # Line Chart history data parsing
    # monthly_logs = logs_qs.annotate(month=TruncMonth('log_date')).values('month').annotate(hours=Sum('total_spent_hrs')).order_by('month')
    # charts['monthly_hours'] = _chart_payload(
    #     [row['month'].strftime('%b %Y'] if row['month'] else 'N/A' for row in monthly_logs],
    #     [float(row['hours'] or 0) for row in monthly_logs],
    #     ['#4f46e5']
    # )
    # 1. Base Overall Timeline (Current View)
    monthly_logs = logs_qs.annotate(month=TruncMonth('log_date')).values('month').annotate(hours=Sum('total_spent_hrs')).order_by('month')
    months_labels = [row['month'].strftime('%b %Y') if row['month'] else 'N/A' for row in monthly_logs]
    
    charts['monthly_hours'] = _chart_payload(
        months_labels,
        [float(row['hours'] or 0) for row in monthly_logs],
        ['#4f46e5']
    )

    # 2. Advanced Multi-Line Breakdown: Grouped by Project Hierarchy
    proj_trend_rows = logs_qs.annotate(month=TruncMonth('log_date'))\
                             .values('month', 'project__project_name')\
                             .annotate(hours=Sum('total_spent_hrs'))\
                             .order_by('month')
                             
    # Structure data payload for unique project arrays
    unique_projects = list(set(r['project__project_name'] for r in proj_trend_rows if r['project__project_name']))
    project_datasets = {p: [0.0] * len(months_labels) for p in unique_projects}
    
    for row in proj_trend_rows:
        if row['month'] and row['project__project_name']:
            m_str = row['month'].strftime('%b %Y')
            if m_str in months_labels:
                idx = months_labels.index(m_str)
                project_datasets[row['project__project_name']][idx] = float(row['hours'] or 0)

    charts['timeline_by_project'] = {
        'labels': months_labels,
        'datasets': [{'label': name, 'data': data} for name, data in project_datasets.items()]
    }

    # 3. Advanced Multi-Line Breakdown: Grouped by Operator/User Hierarchy
    user_trend_rows = logs_qs.annotate(month=TruncMonth('log_date'))\
                             .values('month', 'user__name')\
                             .annotate(hours=Sum('total_spent_hrs'))\
                             .order_by('month')
                             
    unique_users = list(set(r['user__name'] for r in user_trend_rows if r['user__name']))
    user_datasets = {u: [0.0] * len(months_labels) for u in unique_users}
    
    for row in user_trend_rows:
        if row['month'] and row['user__name']:
            m_str = row['month'].strftime('%b %Y')
            if m_str in months_labels:
                idx = months_labels.index(m_str)
                user_datasets[row['user__name']][idx] = float(row['hours'] or 0)

    charts['timeline_by_user'] = {
        'labels': months_labels,
        'datasets': [{'label': name, 'data': data} for name, data in user_datasets.items()]
    }

    # Dropdowns structuring arrays
    filter_options = {
        'projects': list(ProjectMaster.objects.values('id', 'project_name')),
        'users': list(UserMaster.objects.values('id', 'name')),
        'selected_project': project_filter,
        'selected_user': user_filter,
        'selected_date': date_filter,
    }

    recent_activities = list(activities_qs.order_by('-timestamp')[:8].values('action', 'activity_type', 'timestamp'))
    for item in recent_activities:
        item['timestamp'] = timezone.localtime(item['timestamp']).strftime('%d %b %Y, %H:%M')

    recent_logs = list(logs_qs.select_related('project', 'user').order_by('-log_date')[:8].values('log_date', 'total_spent_hrs', 'project__project_name', 'user__name'))
    for item in recent_logs:
        item['log_date'] = item['log_date'].strftime('%d %b %Y')
        item['total_spent_hrs'] = float(item['total_spent_hrs'])

    return {
        'dashboard_totals': totals,
        'dashboard_charts': charts,
        'dashboard_recent_activities': recent_activities,
        'dashboard_recent_logs': recent_logs,
        'filter_options': filter_options,
    }