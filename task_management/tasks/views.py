from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth.models import User
from .models import Task, UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, 
    TaskSerializer, TaskUpdateSerializer, TaskReportSerializer
)
from .permissions import IsAdmin, IsSuperAdmin, IsTaskOwner, IsTaskAdmin
from rest_framework.exceptions import ValidationError
from .utils import assign_task_permissions



# JWT Authentication views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# User viewset for SuperAdmin
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]
    
    def perform_create(self, serializer):
        user = serializer.save()

    
    @action(detail=True, methods=['patch'], serializer_class=UserProfileSerializer)
    def set_role(self, request, pk=None):
        user = self.get_object()
        profile = user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            updated_profile = serializer.save()
            
            # Assign permissions if role is set to ADMIN
            if updated_profile.role == 'ADMIN':
                assign_task_permissions(user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Task viewset for Admin and SuperAdmin
class AdminTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdmin]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'], serializer_class=TaskReportSerializer)
    def report(self, request, pk=None):
        task = self.get_object()
        if task.status != 'COMPLETED':
            return Response({"error": "Report is only available for completed tasks."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskReportSerializer(task)
        return Response(serializer.data)

# User Task API views
class UserTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class UserTaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskOwner]
    
    def perform_update(self, serializer):
        # Validate completion report and worked hours if status is being set to COMPLETED
        instance = self.get_object()
        if serializer.validated_data.get('status') == 'COMPLETED':
            if not serializer.validated_data.get('completion_report'):
                raise serializers.ValidationError({"completion_report": "Completion report is required when marking a task as completed."})
            if not serializer.validated_data.get('worked_hours'):
                raise serializers.ValidationError({"worked_hours": "Worked hours must be provided when marking a task as completed."})
        serializer.save()

class TaskReportView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskAdmin]
    
    def get_object(self):
        task = super().get_object()
        if task.status != 'COMPLETED':
            raise ValidationError({"error": "Report is only available for completed tasks."})

        return task
    


