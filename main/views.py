from django.shortcuts import render
from applicants.models import Vacancy
from django.shortcuts import render, get_object_or_404
from applicants.models import Resume

def index(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'main/index.html', {'vacancies': vacancies})

def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    user_has_resume = Resume.objects.filter(user=request.user).exists()
    return render(request, 'main/job_detail.html', {'vacancy': vacancy, 'user_has_resume': user_has_resume})
