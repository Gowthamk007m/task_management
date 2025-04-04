from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, AdminTaskViewSet, 
    UserTaskListView, UserTaskUpdateView, TaskReportView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'admin/tasks', AdminTaskViewSet)

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Admin API
    path('', include(router.urls)),
    
    # User API
    path('tasks/', UserTaskListView.as_view(), name='user-tasks'),
    path('tasks/<int:pk>/', UserTaskUpdateView.as_view(), name='update-task'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
]