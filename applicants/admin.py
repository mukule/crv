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


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'academic_level', 'area_of_study', 'specialization', 'examining_body',
                    'institution_name', 'admission_number', 'start_year', 'end_year', 'graduation_year',
                    'get_academic_details', 'course_name', 'institution', 'certification', 'start_date',
                    'completion_date', 'get_relevant_courses', 'company_name', 'position',
                    'position_description', 'employment_start_date', 'employment_end_date',
                    'get_employment_histories', 'referee_name', 'occupation', 'organization',
                    'relationship_period', 'email', 'phone', 'get_referees')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_academic_details(self, obj):
        academic_details = obj.academic_details.all()
        return ', '.join(str(academic) for academic in academic_details)

    def get_relevant_courses(self, obj):
        relevant_courses = obj.relevant_courses.all()
        return ', '.join(str(course) for course in relevant_courses)

    def get_employment_histories(self, obj):
        employment_histories = obj.employment_histories.all()
        return ', '.join(str(history) for history in employment_histories)

    def get_referees(self, obj):
        referees = obj.referees.all()
        return ', '.join(str(referee) for referee in referees)

    get_full_name.short_description = 'Full Name'
    get_academic_details.short_description = 'Academic Details'
    get_relevant_courses.short_description = 'Relevant Courses'
    get_employment_histories.short_description = 'Employment Histories'
    get_referees.short_description = 'Referees'

class CustomUserAdmin(UserAdmin):
    inlines = (AcademicDetailsInline, RelevantCourseInline,)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vacancy)
admin.site.register(AcademicDetails)
admin.site.register(RelevantCourse)
admin.site.register(Resume, ResumeAdmin)
