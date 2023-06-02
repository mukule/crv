from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.index, name="index"),
    path('register', views.register, name='register'),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('profile/<username>', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('academic_details', views.create_academic_details, name='academic_details'),
    path('academic_details/update/<int:academic_details_id>', views.update_academic_details, name='update_academic_details'),
    path('relevant_courses/', views.create_relevant_course, name='relevant_courses'),
    path('relevant_course/update/<int:relevant_course_id>/', views.update_relevant_course, name='update_relevant_course'),
    path('employment_history', views.create_employment_history, name='employment_history'),
    path('employment_history/update/<int:employment_history_id>/', views.update_employment_history, name='update_employment_history'),
    path('referee/', views.create_referee, name='referee'),
    path('save-resume/', views.save_resume, name='save_resume'),
    path('referee/update/<int:referee_id>/', views.update_referee, name='update_referee'),
    # path('applicants/resume/export/<int:resume_id>/', views.export_resume_to_excel, name='export_resume_to_excel'),
    

    

]