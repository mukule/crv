from django.urls import path
from . import views
from applicants.views import apply_job
from .views import ResumeView

urlpatterns = [

    path("", views.home, name="home"),
    path("vacancy", views.vacancy, name="vacancy"),
    path('vacancy/<int:vacancy_id>/', views.vacancy_detail, name='job_detail'),
    path('apply_job/<int:vacancy_id>/', apply_job, name='apply_job'),
    path('internships/', views.internships, name='internships'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('internal-adverts/', views.internal_adverts, name='internal_adverts'),
    path('application/status/', views.application_status, name='application_status'),
    path('closed-vacancies/', views.closed_vacancies, name='closed_vacancies'),

]