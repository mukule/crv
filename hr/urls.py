from django.urls import path
from . import views


app_name = 'hr'
urlpatterns = [
    path("", views.index, name="index"),
    path("regs", views.regs, name="regs"),
    path("vac", views.vac, name="vac"),
    path("create_vac", views.create_vac, name="create_vac"),
    path('edit_vacancy/<int:vacancy_id>/', views.edit_vac, name='edit_vac'),
    path("vac_ap", views.vac_ap, name="vac_ap"),
    path('vac_ap_detail/<int:vacancy_id>/',
         views.vac_ap_detail, name='vac_ap_detail'),
    path('toggle_shortlisted/<int:application_id>/',
         views.shortlist, name='shortlist'),
    path('applicant/<int:user_id>/resume/', views.resume, name='resume'),
    path('update_response/<int:application_id>/',
         views.update_response, name='update_response'),
]
