from django.contrib.auth.models import Permission
from .models import Task
from django.contrib.contenttypes.models import ContentType

def assign_task_permissions(user):
    task_ct = ContentType.objects.get_for_model(Task)
    perms = Permission.objects.filter(content_type=task_ct)
    user.user_permissions.set(perms)