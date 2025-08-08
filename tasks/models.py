from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Task(models.Model):
    status_options=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ]

    priority_options = [
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High')
]
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name='tasks')
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=status_options, default='pending')
    priority = models.IntegerField(choices=priority_options, default=2)
    due_date=models.DateField(null=True, blank=True)
    assigned_to=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    