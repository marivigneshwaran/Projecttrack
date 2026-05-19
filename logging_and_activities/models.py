from django.db import models
from customer_and_projects.models import ProjectMaster
from tasks_and_subtasks.models import TaskMaster
from authentication_and_users.models import UserMaster


class LogMaster(models.Model):
    
    project = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE, related_name='project_logs')
    task = models.ForeignKey(TaskMaster, on_delete=models.CASCADE, related_name='task_logs')
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name='user_logs')
    log_date = models.DateField("Log Date")
    total_spent_hrs = models.DecimalField("Total Spent Hrs", max_digits=5, decimal_places=2, default=0.00)
    note = models.TextField("Notes", max_length=500, blank=True) 

    def __str__(self):
        return f"Log: {self.project.project_name} - {self.log_date}"

class ActivityLog(models.Model):
    ACTIVITY_CHOICES = [('inprogress', 'InProgress'), ('completed', 'Completed'), ('drop', 'Drop')]

    action = models.CharField("Action", max_length=255)
    activity_type = models.CharField(max_length=15, choices=ACTIVITY_CHOICES, default='inprogress')
    description = models.TextField("Description", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} at {self.timestamp}"