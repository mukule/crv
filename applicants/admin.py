from django.contrib import admin
from .models import Vacancy, CustomUser, AcademicLevel, AreaOfStudy, Specialization, ExaminingBody, Course

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


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'job_ref', 'date_open', 'date_closed')
    list_filter = ('date_open', 'date_closed')
    search_fields = ('job_name', 'job_ref')
    date_hierarchy = 'date_open'

admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(CustomUser)


