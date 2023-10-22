from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from applicants.models import *
from django.core.paginator import *
from django.db.models import Q
from django.db.models import Count
from applicants.forms import *
from django.contrib import messages

# Create your views here.


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def index(request):
    return render(request, 'hr/index.html')


@user_passes_test(is_superuser)
def regs(request):
    # Get the search query from the request GET parameters
    search_query = request.GET.get('search', '')
    show_all = request.GET.get('show_all')

    # Start with all users (non-superusers)
    users = CustomUser.objects.filter(is_superuser=False)

    if search_query:
        # Filter by username, first name, and last name
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    if show_all:
        # If the "Show All" button is clicked, remove the search filter
        users = CustomUser.objects.filter(is_superuser=False)

    user_count = users.count()

    # Pagination
    paginator = Paginator(users, 100)  # Show 100 users per page
    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'hr/regs.html', {'users': users, 'search_query': search_query, 'user_count': user_count})


@user_passes_test(is_superuser)
def vac(request):
    # Get the values of query parameters (if they exist)
    job_name = request.GET.get('job_name')
    vacancy_type = request.GET.get('vacancy_type')
    job_ref = request.GET.get('job_ref')
    show_all = request.GET.get('show_all')

    # Start with an unfiltered queryset
    vacancies = Vacancy.objects.all().order_by('-date_created')
    if show_all:
        vacancies = Vacancy.objects.all().order_by('-date_created')

    # Apply filters based on query parameters
    if job_name:
        vacancies = vacancies.filter(
            job_name__icontains=job_name)  # Case-insensitive filter

    if vacancy_type:
        # Case-insensitive filter on vacancy type name
        vacancies = vacancies.filter(
            vacancy_type__name__icontains=vacancy_type)

    if job_ref:
        vacancies = vacancies.filter(
            job_ref__icontains=job_ref)  # Case-insensitive filter

    vacancies = vacancies.annotate(application_count=Count('jobapplication'))

    vac_count = vacancies.count()

    # Paginate the list of vacancies by 10 items per page
    paginator = Paginator(vacancies, 10)
    page = request.GET.get('page')

    try:
        vacancies = paginator.page(page)
    except PageNotAnInteger:
        vacancies = paginator.page(1)
    except EmptyPage:
        vacancies = paginator.page(paginator.num_pages)

    return render(request, 'hr/vac.html', {'vacancies': vacancies, 'vac_count': vac_count})


@user_passes_test(is_superuser)
def create_vac(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vacancy created successfully.')
            return redirect('hr:vac')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message = "Vacancy creation failed. Please check the form. Errors: " + \
                ', '.join(error_messages)
            messages.error(request, error_message)
    else:
        form = VacancyForm()

    return render(request, 'hr/create_vac.html', {'form': form})


@user_passes_test(is_superuser)
def edit_vac(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    if request.method == 'POST':
        form = VacancyForm(request.POST, request.FILES, instance=vacancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vacancy updated successfully.')
            return redirect('hr:vac')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message = "Vacancy update failed. Please check the form. Errors: " + \
                ', '.join(error_messages)
            messages.error(request, error_message)
    else:
        form = VacancyForm(instance=vacancy)

    return render(request, 'hr/edit_vacancy.html', {'form': form, 'vacancy': vacancy})


@user_passes_test(is_superuser)
def vac_ap(request):
    # Query to retrieve all vacancies along with the number of applications for each,
    job_name = request.GET.get('job_name')
    vacancy_type = request.GET.get('vacancy_type')
    job_ref = request.GET.get('job_ref')
    show_all = request.GET.get('show_all')
    # ordered by the latest vacancies first
    vacancies = Vacancy.objects.annotate(
        application_count=Count('jobapplication')).order_by('-date_open')

    if show_all:
        vacancies = Vacancy.objects.all().order_by('-date_created')

    # Apply filters based on query parameters
    if job_name:
        vacancies = vacancies.filter(
            job_name__icontains=job_name)  # Case-insensitive filter

    if vacancy_type:
        # Case-insensitive filter on vacancy type name
        vacancies = vacancies.filter(
            vacancy_type__name__icontains=vacancy_type)

    if job_ref:
        vacancies = vacancies.filter(
            job_ref__icontains=job_ref)  # Case-insensitive filter

    vacancies = vacancies.annotate(application_count=Count('jobapplication'))

    vac_count = vacancies.count()

    # Paginate the list of vacancies by 10 items per page
    paginator = Paginator(vacancies, 10)
    page = request.GET.get('page')

    try:
        vacancies = paginator.page(page)
    except PageNotAnInteger:
        vacancies = paginator.page(1)
    except EmptyPage:
        vacancies = paginator.page(paginator.num_pages)

    context = {
        'vacancies': vacancies,
        'vac_count': vac_count
    }

    return render(request, 'hr/ap.html', context)


@user_passes_test(is_superuser)
def vac_ap_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    applications = JobApplication.objects.filter(vacancy=vacancy)

    # Search functionality
    search_query = request.GET.get('search')
    show_all = request.GET.get('show_all')

    if search_query:
        # Filter by username, first name, and last name within job applications
        applications = applications.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    if show_all:
        # If the "Show All" button is clicked, remove the search filter
        applications = JobApplication.objects.filter(vacancy=vacancy)

    vac_count = applications.count()
    # Pagination
    paginator = Paginator(applications, 20)  # Show 10 applications per page
    page = request.GET.get('page')
    applications = paginator.get_page(page)

    context = {
        'vacancy': vacancy,
        'applications': applications,
        'search_query': search_query,
        'vac_count': vac_count
    }

    return render(request, 'hr/vac_ap_detail.html', context)
