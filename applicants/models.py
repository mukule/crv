from django.db import models
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Users', self.username, instance)
        return None

    ...
    image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)

class Vacancy(models.Model):
    job_name = models.CharField(max_length=100)
    job_ref = models.CharField(max_length=20)
    job_description = models.TextField()
    reports_to = models.CharField(max_length=100)
    requirements = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    date_open = models.DateField()
    date_closed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_name} (Vacancy: {self.job_ref})"
