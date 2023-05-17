from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Vacancy, CustomUser, AcademicLevel, AreaOfStudy, Specialization, ExaminingBody, Course, AcademicDetails

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


class CustomUserAdmin(UserAdmin):
    inlines = (AcademicDetailsInline,)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vacancy)
admin.site.register(AcademicDetails)
