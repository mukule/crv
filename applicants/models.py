from django.db import models
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, blank=True)
    postal_address = models.CharField(max_length=255, blank=True)

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Users', self.username, instance)
        return None

    image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)

    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None


class AcademicLevel(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.level

class AreaOfStudy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Specialization(models.Model):
    area_of_study = models.ForeignKey(AreaOfStudy, on_delete=models.CASCADE, related_name='specializations')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExaminingBody(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True)
    examining_body = models.ForeignKey(ExaminingBody, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class AcademicDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True, blank=True)
    area_of_study = models.ForeignKey(AreaOfStudy, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    examining_body = models.ForeignKey(ExaminingBody, on_delete=models.SET_NULL, null=True, blank=True)
    institution_name = models.CharField(max_length=100, null=True, blank=True)
    admission_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)
    graduation_year = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class RelevantCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    provider = models.ForeignKey(ExaminingBody, on_delete=models.SET_NULL, null=True, blank=True)
    completion_date = models.DateField()

    def __str__(self):
        return self.course_name





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
