from django.contrib.auth import get_user_model

def create_admin_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='admin'
        )