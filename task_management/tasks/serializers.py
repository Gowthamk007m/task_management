from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(source='profile.role', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 🔐 Hash it
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_username',
            'created_by', 'created_by_username', 'due_date', 'status',
            'completion_report', 'worked_hours', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError("Completion report is required when marking a task as completed.")
            if not data.get('worked_hours'):
                raise serializers.ValidationError("Worked hours must be provided when marking a task as completed.")
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completion_report', 'worked_hours']