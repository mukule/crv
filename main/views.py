from django.shortcuts import render
from applicants.models import Vacancy
from django.shortcuts import render, get_object_or_404
from applicants.models import Resume
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from applicants.forms import JobSearchForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def index(request):
    current_date = timezone.now().date()
    all_employment_vacancies = Vacancy.objects.filter(vacancy_type__name='Employment', date_open__lte=current_date, date_closed__gte=current_date)
    form = JobSearchForm()
    
    if request.method == 'GET' and 'search' in request.GET:
        form = JobSearchForm(request.GET)
        if form.is_valid():
            # Process the form data and filter the vacancies accordingly
            keywords = form.cleaned_data['keywords']
            area_of_study = form.cleaned_data['area_of_study']
            specialization = form.cleaned_data['specialization']
            department = form.cleaned_data['department']
            vacancy_type = form.cleaned_data['vacancy_type']
            
            print(area_of_study)
            print(all_employment_vacancies)
            # Apply the search filters on the all_employment_vacancies queryset
            employment_vacancies = all_employment_vacancies.filter(
            Q(job_name__icontains=keywords) |
            Q(area_of_study=area_of_study) |
            Q(specialization=specialization) |
            Q(department__icontains=department) |
            Q(vacancy_type=vacancy_type)
            )
            print("fltered employemnt Vacancy",employment_vacancies)
            
            if not employment_vacancies.exists():
                # If no job matches the search criteria, display a message
                messages.info(request, "No jobs match the search criteria.")
    
    else:
        employment_vacancies = all_employment_vacancies
    
    return render(request, 'main/index.html', {'form': form, 'vacancies': employment_vacancies})



@login_required
def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    user_has_resume = Resume.objects.filter(user=request.user).exists()
    return render(request, 'main/job_detail.html', {'vacancy': vacancy, 'user_has_resume': user_has_resume})

def internships(request):
    current_date = timezone.now().date()
    all_internship_vacancies = Vacancy.objects.filter(vacancy_type__name='Internship', date_open__lte=current_date, date_closed__gte=current_date)
    form = JobSearchForm()
    
    if request.method == 'GET' and 'search' in request.GET:
        form = JobSearchForm(request.GET)
        if form.is_valid():
            # Process the form data and filter the internships accordingly
            keywords = form.cleaned_data['keywords']
            area_of_study = form.cleaned_data['area_of_study']
            specialization = form.cleaned_data['specialization']
            department = form.cleaned_data['department']
            vacancy_type = form.cleaned_data['vacancy_type']
            
            # Apply the search filters on the all_internship_vacancies queryset
            internship_vacancies = all_internship_vacancies.filter(
                Q(job_name__icontains=keywords) |
                Q(area_of_study=area_of_study) |
                Q(specialization=specialization) |
                Q(department__icontains=department) |
                Q(vacancy_type=vacancy_type)
            )
            
            if not internship_vacancies.exists():
                # If no internships match the search criteria, display a message
                messages.info(request, "No internships match the search criteria.")
    
    else:
        internship_vacancies = all_internship_vacancies
    
    return render(request, 'main/internships.html', {'form': form, 'vacancies': internship_vacancies})

@method_decorator(login_required, name='dispatch')
class ResumeView(TemplateView):
    template_name = 'main/resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        resume = Resume.objects.filter(user=user).first()

        if resume:
            academic_details = resume.academic_details.all()
            relevant_courses = resume.relevant_courses.all()
            employment_histories = resume.employment_histories.all()
            referees = resume.referees.all()

            context['resume'] = resume
            context['academic_details'] = academic_details
            context['relevant_courses'] = relevant_courses
            context['employment_histories'] = employment_histories
            context['referees'] = referees

        return context