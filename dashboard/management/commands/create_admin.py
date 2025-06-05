from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = "himanshu_17lodhi"
        email = "lodhihimanshu@gmail.com"
        password = "Jairajputana@17"
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created!")
        else:
            print("Superuser already exists.")