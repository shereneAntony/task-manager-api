from django.urls import path
from .views import AddListProject, TaskListCreate, ProjectDetails, TaskDetails



urlpatterns = [
    path('projects/', AddListProject.as_view(), name='add-list-projects'),
    path('projects/<int:id>/', ProjectDetails.as_view(), name='projects-details'),
    path('tasks/', TaskListCreate.as_view(), name='add-list-tasks'),
    path('tasks/<int:id>/', TaskDetails.as_view(), name='tasks-details')
]
