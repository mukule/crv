from django.shortcuts import render
from applicants.models import Vacancy
from django.shortcuts import render, get_object_or_404
from applicants.models import Resume

from django.utils import timezone

def index(request):
    current_date = timezone.now().date()
    open_vacancies = Vacancy.objects.filter(date_open__lte=current_date, date_closed__gte=current_date)
    return render(request, 'main/index.html', {'vacancies': open_vacancies})


def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    user_has_resume = Resume.objects.filter(user=request.user).exists()
    return render(request, 'main/job_detail.html', {'vacancy': vacancy, 'user_has_resume': user_has_resume})
