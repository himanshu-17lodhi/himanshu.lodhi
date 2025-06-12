import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "himanshu_lodhi"
email = "lodhihimanshu17@gmail.com"
password = "Jairajputana@17"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created!")
else:
    print("Superuser already exists.")