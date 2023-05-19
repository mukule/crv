from django.shortcuts import render
from applicants.models import Vacancy
from django.shortcuts import render, get_object_or_404

def index(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'main/index.html', {'vacancies': vacancies})

def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    return render(request, 'main/job_detail.html', {'vacancy': vacancy})
