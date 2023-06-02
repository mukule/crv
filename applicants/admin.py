from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ExportMixin
from import_export import resources
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms




@admin.register(AcademicLevel)
class AcademicLevelAdmin(admin.ModelAdmin):
    list_display = ('level',)


@admin.register(AreaOfStudy)
class AreaOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'area_of_study')


@admin.register(ExaminingBody)
class ExaminingBodyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'examining_body')


class AcademicDetailsInline(admin.TabularInline):
    model = AcademicDetails
    extra = 0


class RelevantCourseInline(admin.TabularInline):
    model = RelevantCourse
    extra = 0

class ResumeResource(resources.ModelResource):
    class Meta:
        model = Resume



@admin.register(Resume)
class ResumeAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ResumeResource
    list_display = (
        'get_full_name',
        'get_email',
        'get_phone',
        'get_academic_level',
        'get_area_of_study',
        'get_specialization',
        'get_examining_body',
        'get_other_courses',
        'get_institution',
        'get_experience',
        'get_referee',
    )

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_email(self, obj):
        return obj.user.email

    def get_phone(self, obj):
        return obj.user.phone

    def get_academic_level(self, obj):
        academic_details = obj.academic_details.all()
        return ', '.join(str(academic.academic_level) for academic in academic_details)

    def get_area_of_study(self, obj):
        academic_details = obj.academic_details.all()
        return ', '.join(str(academic.area_of_study) for academic in academic_details)

    def get_specialization(self, obj):
        academic_details = obj.academic_details.all()
        return ', '.join(str(academic.specialization) for academic in academic_details)

    def get_examining_body(self, obj):
        academic_details = obj.academic_details.all()
        return ', '.join(str(academic.examining_body) for academic in academic_details)

    def get_institution(self, obj):
        return ', '.join(
            f"{course.institution} ({course.certification})" for course in obj.relevant_courses.all()
        )

    def get_other_courses(self, obj):
        return ', '.join(str(course.course_name) for course in obj.relevant_courses.all())

    def get_experience(self, obj):
        employment_histories = obj.employment_histories.all()
        experience_list = []
        for history in employment_histories:
            experience = f"{history.company_name} - {history.position}"
            if history.start_date and history.end_date:
                start_year = history.start_date.year
                end_year = history.end_date.year
                years_of_experience = end_year - start_year
                experience += f" ({years_of_experience} years)"
            experience_list.append(experience)
        return ', '.join(experience_list)


    def get_referee(self, obj):
        return ', '.join(
            f"{referee.name} ({referee.organization})" for referee in obj.referees.all()
        )
    
    

    get_full_name.short_description = 'Full Name'
    get_email.short_description = 'Email'
    get_phone.short_description = 'Phone'
    get_academic_level.short_description = 'Academic Level'
    get_area_of_study.short_description = 'Area of Study'
    get_specialization.short_description = 'Specialization'
    get_examining_body.short_description = 'Examiner'
    get_other_courses.short_description = 'Other Courses'
    get_institution.short_description = 'Institution'
    get_experience.short_description = 'Experience'
    get_referee.short_description = 'Referee'
    
    list_filter = (
        'academic_details__academic_level',
        'academic_details__area_of_study',
        'academic_details__specialization',
        'academic_details__examining_body',
    )

    list_export = (
        'get_full_name',
        'get_email',
        'get_phone',
        'get_academic_level',
        'get_area_of_study',
        'get_specialization',
        'get_examining_body',
        'get_other_courses',
        'get_institution',
        'get_experience',
        'get_referee',
    )

@admin.register(VacancyType)
class VacancyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    


class VacancyNameFilter(admin.SimpleListFilter):
    title = 'Vacancy Name'
    parameter_name = 'vacancy_name'

    def lookups(self, request, model_admin):
        vacancies = Vacancy.objects.all().values_list('id', 'job_name')
        return vacancies

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vacancy__id=self.value())

from import_export import fields

class JobApplicationResource(resources.ModelResource):
    user_full_name = fields.Field(attribute='user__get_full_name', column_name='User')
    vacancy_name = fields.Field(attribute='vacancy__job_name', column_name='Vacancy')
    is_qualified = fields.Field(column_name='Is Qualified')

    class Meta:
        model = JobApplication
        fields = ('user_full_name', 'vacancy_name', 'application_date', 'is_qualified')

    def dehydrate_is_qualified(self, obj):
        return 'Yes' if obj.is_qualified else 'No'

class JobApplicationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = JobApplicationResource
    list_display = ('get_user_full_name', 'get_vacancy_name', 'application_date', 'get_is_qualified', 'get_resume_details',)
    list_filter = ('application_date', 'vacancy__job_name', 'is_qualified')
    actions = ['send_email_to_applicants']

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()

    get_user_full_name.short_description = 'User'

    def get_vacancy_name(self, obj):
        return obj.vacancy.job_name

    get_vacancy_name.short_description = 'Vacancy'

    def get_is_qualified(self, obj):
        return 'Yes' if obj.is_qualified else 'No'

    get_is_qualified.short_description = 'Is Qualified'

    def get_resume_details(self, obj):
        user_id = obj.user.id
        resume_link = reverse('admin:applicants_resume_changelist') + f"?user__id__exact={user_id}"
        return format_html('<a href="{}">{}</a>', resume_link, 'View Resume')

    get_resume_details.short_description = 'Resume Details'

    
        

    class EmailForm(forms.Form):
        template = forms.ModelChoiceField(queryset=EmailTemplate.objects.all())

    def send_email_to_applicants(self, request, queryset):
        for application in queryset:
            from_email = 'admin@example.com'
            to_email = [application.user.email]

            # Customize the email subject and message for each applicant
            subject = f'Regarding Your Job Application for {application.vacancy.job_name}'
            message = f"Dear {application.user.get_full_name()}, we are happy to let you know that you qualified for the first phase of recruitment for the job you applied for: {application.vacancy.job_name}. Congratulations!!, We will let you know on the next process"

            send_mail(subject, message, from_email, to_email)

        self.message_user(request, 'Emails have been sent to selected applicants.')

    send_email_to_applicants.short_description = 'Send email to selected applicants'
    actions = [send_email_to_applicants]


    
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'interest', 'is_organization_staff')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'full_name', 'email', 'interest', 'is_staff', 'is_superuser', 'is_organization_staff')

    inlines = (AcademicDetailsInline, RelevantCourseInline,)

    def full_name(self, obj):
        return obj.get_full_name()

    full_name.short_description = 'Name'

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['subject']




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vacancy)
admin.site.register(AcademicDetails)
admin.site.register(RelevantCourse)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)

