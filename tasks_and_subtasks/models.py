from django.db import models

class TaskListMaster(models.Model):
    STATUS = [('inprogress', 'InProgress'), ('completed', 'Completed'), ('drop', 'Drop')]

    name = models.CharField("Name", max_length=100)
    status = models.CharField(max_length=15, choices=STATUS, default='inprogress')

    def __str__(self):
        return self.name 

class TaskMaster(models.Model):
    PRIORITY = [('hot', 'Hot'), ('cold', 'Cold'), ('normal', 'Normal')]
    STATUS = [('inprogress', 'InProgress'), ('completed', 'Completed'), ('drop', 'Drop')]

    task_name = models.CharField("Name", max_length=200)
    task_list = models.ForeignKey(TaskListMaster, on_delete=models.PROTECT, related_name='tasks')
    priority = models.CharField(max_length=15, choices=PRIORITY, default='normal')
    status = models.CharField(max_length=15, choices=STATUS, default='inprogress')
    estimated_hrs = models.DecimalField("Estimated Hrs", max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.task_name

class SubTaskMaster(models.Model):
    STATUS = [('inprogress', 'InProgress'), ('completed', 'Completed'), ('drop', 'Drop')]

    sub_task_name = models.CharField("Sub Task Name", max_length=200)
    parent_task = models.ForeignKey(TaskMaster, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=15, choices=STATUS, default='inprogress')
    estimated_hrs = models.DecimalField("Estimated Hrs", max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.sub_task_name} (Parent: {self.parent_task.task_name})"

class TaskAssignee(models.Model):
    STATUS = [('inprogress', 'InProgress'), ('billed', 'Billed'), ('pending', 'Pending')]

    task = models.ForeignKey(TaskMaster, on_delete=models.CASCADE, related_name='assignees')
    user = models.ForeignKey(
        'authentication_and_users.UserMaster',
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
    )
    billing_status = models.CharField(max_length=15, choices=STATUS, default='pending')

    def __str__(self):
        return f"{self.user.name} assigned to {self.task.task_name}"    