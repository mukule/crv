from django.shortcuts import render
from applicants.models import Vacancy
from django.shortcuts import render, get_object_or_404
from applicants.models import Resume
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    current_date = timezone.now().date()
    employment_vacancies = Vacancy.objects.filter(vacancy_type__name='Employment', date_open__lte=current_date, date_closed__gte=current_date)
    return render(request, 'main/index.html', {'vacancies': employment_vacancies})

@login_required
def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    user_has_resume = Resume.objects.filter(user=request.user).exists()
    return render(request, 'main/job_detail.html', {'vacancy': vacancy, 'user_has_resume': user_has_resume})

def internships(request):
    current_date = timezone.now().date()
    internship_vacancies = Vacancy.objects.filter(vacancy_type__name='Internship', date_open__lte=current_date, date_closed__gte=current_date)
    return render(request, 'main/internships.html', {'vacancies': internship_vacancies})
