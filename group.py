import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cedus.settings')
import django
django.setup()
from django.contrib.auth.models import Group, Permission, User
from main import models
from main import views

class_1 = Group.objects.get_or_create(name ='class_1')

