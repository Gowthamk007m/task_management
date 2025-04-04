import os
import django
import datetime
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

from django.contrib.auth.models import User
from tasks.models import Task, UserProfile

def create_test_data():
    # Clear existing data (optional)
    # Task.objects.all().delete()
    # UserProfile.objects.all().delete()
    # User.objects.filter(is_superuser=False).delete()

    # Create users with different roles
    # SuperAdmin
    superadmin, created = User.objects.get_or_create(
        username='superadmin',
        defaults={
            'email': 'superadmin@example.com',
            'first_name': 'Super',
            'last_name': 'Admin',
            'is_staff': True,
        }
    )
    if created:
        superadmin.set_password('superadmin123')
        superadmin.save()
        superadmin.profile.role = 'SUPERADMIN'
        superadmin.profile.save()
        print(f"Created SuperAdmin: {superadmin.username}")
    else:
        print(f"SuperAdmin already exists: {superadmin.username}")
    
    # Admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Regular',
            'last_name': 'Admin',
            'is_staff': True,
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        admin.profile.role = 'ADMIN'
        admin.profile.save()
        print(f"Created Admin: {admin.username}")
    else:
        print(f"Admin already exists: {admin.username}")
    
    # Regular users
    users = []
    for i in range(1, 4):
        user, created = User.objects.get_or_create(
            username=f'user{i}',
            defaults={
                'email': f'user{i}@example.com',
                'first_name': f'User {i}',
                'last_name': 'Test',
                'is_staff': False,
            }
        )
        if created:
            user.set_password(f'user{i}123')
            user.save()
            user.profile.role = 'USER'
            user.profile.save()
            print(f"Created User: {user.username}")
        else:
            print(f"User already exists: {user.username}")
        users.append(user)
    
    # Create tasks in different states
    tasks_data = [
        {
            'title': 'Implement Login Page',
            'description': 'Create a responsive login page with forgot password feature',
            'assigned_to': users[0],
            'created_by': admin,
            'due_date': datetime.date.today() + datetime.timedelta(days=5),
            'status': 'PENDING'
        },
        {
            'title': 'Database Schema Design',
            'description': 'Design database schema for the new customer management module',
            'assigned_to': users[1],
            'created_by': admin,
            'due_date': datetime.date.today() + datetime.timedelta(days=3),
            'status': 'IN_PROGRESS'
        },
        {
            'title': 'Bug Fix: Registration Form',
            'description': 'Fix validation issues on the registration form',
            'assigned_to': users[2],
            'created_by': superadmin,
            'due_date': datetime.date.today() + datetime.timedelta(days=1),
            'status': 'IN_PROGRESS'
        },
        {
            'title': 'Create API Documentation',
            'description': 'Document all API endpoints with examples',
            'assigned_to': users[0],
            'created_by': superadmin,
            'due_date': datetime.date.today() - datetime.timedelta(days=1),
            'status': 'COMPLETED',
            'completion_report': 'Created comprehensive API documentation with Swagger UI integration. All endpoints are documented with examples.',
            'worked_hours': Decimal('8.5')
        },
        {
            'title': 'Update Privacy Policy',
            'description': 'Update privacy policy to comply with new regulations',
            'assigned_to': users[1],
            'created_by': admin,
            'due_date': datetime.date.today() - datetime.timedelta(days=2),
            'status': 'COMPLETED',
            'completion_report': 'Updated privacy policy with legal team input. Created new section for data retention policies.',
            'worked_hours': Decimal('4.0')
        }
    ]
    
    for task_data in tasks_data:
        task, created = Task.objects.get_or_create(
            title=task_data['title'],
            defaults=task_data
        )
        if created:
            print(f"Created Task: {task.title}")
        else:
            print(f"Task already exists: {task.title}")
    
    print("Test data creation completed!")

if __name__ == '__main__':
    create_test_data()