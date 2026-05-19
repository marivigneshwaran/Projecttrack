from django.db import models

class CustomerMaster(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    name = models.CharField("Name", max_length=100)
    email = models.EmailField("Email", max_length=100, unique=True)
    phone = models.CharField("Phone", max_length=15)
    address = models.TextField("Address") # Changed to TextField for longer addresses
    active_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self): # Fixed casing from __Str__
        return self.name
    
class ProjectMaster(models.Model):
    PROJECT_TYPE = [('internal', 'Internal'), ('external', 'External')] # Fixed typo 'extenal'
    STATUS = [('inprogress', 'InProgress'), ('completed', 'Completed'), ('drop', 'Drop')]

    project_name = models.CharField("Project Name", max_length=100)
    client = models.ForeignKey(CustomerMaster, on_delete=models.PROTECT, related_name='projects')
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPE, default='internal')
    start_date = models.DateField("Start Date") # Removed auto_now_add to allow manual entry
    due_date = models.DateField("Due Date") # Fixed name from end_date to match requirements
    status = models.CharField(max_length=15, choices=STATUS, default='inprogress')
    progress_percent = models.IntegerField("Progress Percent", default=0)

    def __str__(self):
        return f"{self.project_name} ({self.client.name})"

class PhaseMaster(models.Model):
    STATUS = [('inprogress', 'InProgress'), ('completed', 'Completed'), ('drop', 'Drop')]

    phase_name = models.CharField("Phase Name", max_length=300)
    project = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE, related_name='phases')
    budget = models.DecimalField("Budget", max_digits=12, decimal_places=2)
    start_date = models.DateField("Start Date")
    due_date = models.DateField("Due Date")
    status = models.CharField(max_length=15, choices=STATUS, default='inprogress')

    def __str__(self):
        return f"{self.phase_name} - {self.project.project_name}"