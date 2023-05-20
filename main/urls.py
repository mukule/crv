from django.urls import path
from . import views
from applicants.views import apply_job

urlpatterns = [
    path("", views.index, name="index"),
    path('vacancy/<int:vacancy_id>/', views.vacancy_detail, name='job_detail'),
    path('apply_job/<int:vacancy_id>/', apply_job, name='apply_job'),
]