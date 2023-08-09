from django.db import models
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from ckeditor.fields import RichTextField
from datetime import date
from django.contrib.auth import get_user_model
import time



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
    INTEREST_CHOICES = (
    ('I', 'Internship'),
    ('E', 'Employment'),
)
    interest = models.CharField(max_length=255, choices=INTEREST_CHOICES, blank=True)
    is_organization_staff = models.BooleanField(default=False)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, blank=True)
    postal_address = models.CharField(max_length=255, blank=True)
    DISABILITY_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    is_person_with_disability = models.CharField(max_length=1, choices=DISABILITY_CHOICES, blank=True)
    pwd_no = models.CharField(max_length=255, blank=True)
    

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
    is_studying = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class RelevantCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100, null=True, blank=True)
    certification = models.ForeignKey(ExaminingBody, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(blank=True, null=True)
    is_studying = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class EmploymentHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    position_description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    currently_working_here = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.company_name} - {self.position}"
    
class Referee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    relationship_period = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True, blank=True)
    area_of_study = models.ForeignKey(AreaOfStudy, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    examining_body = models.ForeignKey(ExaminingBody, on_delete=models.SET_NULL, null=True, blank=True, related_name='resume_examining_body')
    institution_name = models.CharField(max_length=100, null=True, blank=True)
    admission_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)
    graduation_year = models.DateField(blank=True, null=True)
    academic_details = models.ManyToManyField(AcademicDetails, blank=True)
    
    # Fields from RelevantCourse model
    course_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100, null=True, blank=True)
    certification = models.ForeignKey(ExaminingBody, on_delete=models.SET_NULL, null=True, blank=True, related_name='resume_certification')
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(blank=True, null=True)
    relevant_courses = models.ManyToManyField(RelevantCourse, blank=True)
    # Fields from EmploymentHistory model
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    position_description = models.TextField(blank=True, null=True)
    employment_start_date = models.DateField(blank=True, null=True)
    employment_end_date = models.DateField(blank=True, null=True)
    employment_histories = models.ManyToManyField(EmploymentHistory, blank=True)
    
    # Fields from Referee model
    referee_name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    relationship_period = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    referees = models.ManyToManyField(Referee, blank=True)

    @property
    def years_of_experience(self):
        if self.employment_start_date and self.employment_end_date:
            today = date.today()
            total_years = today.year - self.employment_start_date.year
            if today.month < self.employment_start_date.month or (today.month == self.employment_start_date.month and today.day < self.employment_start_date.day):
                total_years -= 1
            return total_years
        else:
            return 0

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Resume"
    
class VacancyType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    job_name = models.CharField(max_length=200)
    job_ref = models.CharField(max_length=200)
    job_description = RichTextField(blank=True, null=True)
    reports_to = models.CharField(max_length=200, blank=True, null=True)
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True, blank=True)
    area_of_study = models.ForeignKey(AreaOfStudy, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    requirements = RichTextField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    number_of_vacancies = models.PositiveIntegerField(blank=True, null=True)
    responsibilities = RichTextField(blank=True, null=True)
    vacancy_type = models.ForeignKey(VacancyType, on_delete=models.SET_NULL, null=True, blank=True)
    document = models.FileField(upload_to='vacancy_documents/', blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_open = models.DateField()
    date_closed = models.DateField(null=True, blank=True)
    is_filled = models.BooleanField(default=False)  # New boolean field

    def __str__(self):
        return f"{self.job_name} (Vacancy: {self.job_ref})"


def certificate_upload_to(instance, filename):
    # Save the file with the user's full name
    full_name = f"{instance.user.first_name}_{instance.user.last_name}"
    return f"certificates/{full_name}/{filename}"


def certificate_upload_to(instance, filename):
    # Save the file with the user's full name
    full_name = f"{instance.user.first_name}_{instance.user.last_name}"
    return f"certificates/{full_name}/{filename}"

class Document(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.FileField(upload_to=certificate_upload_to)

    def __str__(self):
        return self.document.name

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a unique filename based on user and timestamp
            timestamp = str(int(time.time()))
            filename = f"{self.user.username}_{timestamp}_{os.path.basename(self.document.name)}"
            self.document.name = filename

        return super().save(*args, **kwargs)


class JobApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    application_date = models.DateTimeField(default=timezone.now)
    cover_letter = models.TextField()
    is_qualified = models.BooleanField(default=False)
    response = models.TextField(blank=True)  # New field for admin's comment

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.vacancy.job_name} Application"

    def delete(self, using=None, keep_parents=False):
        # Delete associated documents
        self.user.documents.all().delete()
        super().delete(using, keep_parents)

    def is_vacancy_open(self):
        return self.vacancy.date_closed is None or self.vacancy.date_closed > timezone.now().date()

