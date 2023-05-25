from django.shortcuts import render
from applicants.models import Vacancy
from django.shortcuts import render, get_object_or_404
from applicants.models import Resume
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from applicants.forms import JobSearchForm
from django.contrib import messages

def index(request):
    current_date = timezone.now().date()
    employment_vacancies = Vacancy.objects.filter(vacancy_type__name='Employment', date_open__lte=current_date, date_closed__gte=current_date)
    
    if request.method == 'GET' and 'search' in request.GET:
        form = JobSearchForm(request.GET)
        if form.is_valid():
            # Process the form data and filter the vacancies accordingly
            keywords = form.cleaned_data['keywords']
            area_of_study = form.cleaned_data['area_of_study']
            specialization = form.cleaned_data['specialization']
            department = form.cleaned_data['department']
            vacancy_type = form.cleaned_data['vacancy_type']
            
            # Filter the vacancies based on the form inputs
            employment_vacancies = employment_vacancies.filter(
                job_name__icontains=keywords,
                area_of_study=area_of_study,
                specialization=specialization,
                department__icontains=department,
                vacancy_type=vacancy_type
            )
            
            if not employment_vacancies:
                # If no job matches the search criteria, display a message
                message = "No jobs match the search criteria."
                messages.info(request, message)
    
    else:
        form = JobSearchForm()
    
    return render(request, 'main/index.html', {'form': form, 'vacancies': employment_vacancies})

    
    return render(request, 'main/index.html', {'form': form, 'vacancies': employment_vacancies})


@login_required
def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    user_has_resume = Resume.objects.filter(user=request.user).exists()
    return render(request, 'main/job_detail.html', {'vacancy': vacancy, 'user_has_resume': user_has_resume})

def internships(request):
    current_date = timezone.now().date()
    internship_vacancies = Vacancy.objects.filter(vacancy_type__name='Internship', date_open__lte=current_date, date_closed__gte=current_date)
    return render(request, 'main/internships.html', {'vacancies': internship_vacancies})
