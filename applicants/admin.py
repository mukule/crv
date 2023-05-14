from django.contrib import admin
from .models import JobApplication

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'job_ref', 'date_open', 'date_closed')
    list_filter = ('date_open', 'date_closed')
    search_fields = ('job_name', 'job_ref')
    date_hierarchy = 'date_open'

admin.site.register(JobApplication, JobApplicationAdmin)
