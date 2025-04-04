from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Task, UserProfile

# Customize User admin to include profile information



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        try:
            return obj.profile.role
        except UserProfile.DoesNotExist:
            return "No Profile"
    
    get_role.short_description = 'Role'

# Register Task model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'status', 'worked_hours')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')
    readonly_fields = ('created_at', 'updated_at')
    
    # Customize admin view permissions based on user role
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not hasattr(request.user, 'profile'):
            return queryset.none()
        
        user_role = request.user.profile.role

        if user_role == 'SUPERADMIN':
            return queryset
        elif user_role == 'ADMIN':
            return queryset.filter(created_by=request.user)  # 👈 Only tasks created by the admin
        return queryset.none()

    
    def has_change_permission(self, request, obj=None):
        if not hasattr(request.user, 'profile'):
            return False
            
        user_role = request.user.profile.role
        return user_role in ['SUPERADMIN', 'ADMIN']
    
    def has_add_permission(self, request):
        if not hasattr(request.user, 'profile'):
            return False
            
        user_role = request.user.profile.role
        return user_role in ['SUPERADMIN', 'ADMIN']
    
    def has_delete_permission(self, request, obj=None):
        if not hasattr(request.user, 'profile'):
            return False
            
        user_role = request.user.profile.role
        return user_role in ['SUPERADMIN', 'ADMIN']


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)