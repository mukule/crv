from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('vacancy/<int:vacancy_id>/', views.vacancy_detail, name='job_detail'),
]