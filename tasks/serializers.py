from rest_framework import serializers
from django.contrib.auth.models import User
from.models import Project, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'due_date',
            'created_at', 'updated_at', 'assigned_to', 'project'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProjectDetailSerializer(serializers.ModelSerializer):
    tasks=TaskSerializer(many=True, read_only=True)

    class Meta:
        model=Project
        fields=['id','name','description','created_by','created_at','updated_at','tasks']