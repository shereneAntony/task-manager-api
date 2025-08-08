from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .tasks import send_task_notification_email
from .serializers import ProjectSerializer, TaskSerializer, ProjectDetailSerializer
from .models import Project, Task
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
# Create your views here.


class AddListProject(ListCreateAPIView):
    serializer_class=ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProjectDetails(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field='id'
    
    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method== 'GET':
            return ProjectDetailSerializer
        return ProjectSerializer
    

class TaskListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'priority': ['exact'],
        'due_date': ['exact', 'gte', 'lte'],
        'project': ['exact'],
    }
    ordering_fields = ['priority', 'due_date']

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save()
        if task.assigned_to and task.assigned_to.email:
            send_task_notification_email.delay(
                task.assigned_to.email,
                "Task Assigned",
                f"You have been assigned the task: {task.title}"
            )


class TaskDetails(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        old_task = self.get_object()
        old_status = old_task.status  # ✅ store old status before save
        task = serializer.save()

        if task.status != old_status and task.assigned_to and task.assigned_to.email:
            send_task_notification_email.delay(
                task.assigned_to.email,
                "Task Status Updated",
                f"The status of your task '{task.title}' is now '{task.status}'."
            )
