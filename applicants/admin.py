from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


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

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'get_academic_level',
        'get_area_of_study',
        'get_specialization',
        'get_examining_body',
        'get_other_courses',
        'get_institution',
        'get_experience',
        'get_referee'
    )

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

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
        return ', '.join(f"{history.company_name} - {history.position}" for history in employment_histories)

    def get_referee(self, obj):
        return ', '.join(
            f"{referee.name} ({referee.organization})" for referee in obj.referees.all()
        )

    get_full_name.short_description = 'Full Name'
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



class CustomUserAdmin(UserAdmin):
    inlines = (AcademicDetailsInline, RelevantCourseInline,)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vacancy)
admin.site.register(AcademicDetails)
admin.site.register(RelevantCourse)

