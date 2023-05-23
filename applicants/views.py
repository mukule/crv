from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .token import account_activation_token
from django.core.mail import EmailMessage
from .forms import *
from django.db.models.query_utils import Q
from .models import *
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import csv
from django.http import HttpResponse
from django.http import HttpResponse
from .resources import ResumeResource
from tablib import Dataset

User = get_user_model()



# Create your views here.


def index(request):
    return render('main/index.html')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('applicants/applicant_activate_account.html', {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Account registered succesfully for {user.first_name} {user.last_name} Check your mail {to_email} to activate the account.')
    else:
        messages.error(request, f'If you did not receive the email, Please confirm that {to_email} this is your actual mail')


@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('index')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegisterForm()

    return render(
        request=request,
        template_name="applicants/register.html",
        context={"form": form}
        )

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thanks for your email confirmation. Log in now ')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('login')



@user_not_authenticated
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"You have succesfully logged in as {user.first_name} {user.last_name}")
                return redirect('index')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = AuthenticationForm() 
    
    return render(
        request=request,
        template_name="applicants/login.html", 
        context={'form': form}
        )

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'applicants/password_reset_confirm.html', {'form': form})


@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("applicants/applicant_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, "Password reset link has been send to your email")
                else:
                    messages.error(request, "Problem sending reset password email, SERVER PROBLEM")

            return redirect('index')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="applicants/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your reset succesfully, Login now")
                return redirect('index')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'applicants/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("index")
@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "succesfully logged out")
    return redirect("index")


def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            success_message = f'{user_form.first_name} {user_form.last_name}, your Personnal information has been updated!'
            messages.success(request, success_message)
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'applicants/profile.html', context={'form': form})

    return redirect("index")



@login_required
def create_academic_details(request):
    user = request.user

    academic_details = AcademicDetails.objects.filter(user=user)

    if request.method == 'POST':
        form = AcademicDetailsForm(request.POST)
        if form.is_valid():
            academic_detail = form.save(commit=False)
            academic_detail.user = user
            academic_detail.save()
            messages.success(request, 'Academic details created successfully.')
            return redirect('academic_details')

    else:
        form = AcademicDetailsForm()

    context = {
        'form': form,
        'academic_details': academic_details
    }

    return render(request, 'applicants/academic_details.html', context)



def update_academic_details(request, academic_details_id):
    academic_details = get_object_or_404(AcademicDetails, id=academic_details_id, user=request.user)

    if request.method == 'POST':
        form = AcademicDetailsForm(request.POST, instance=academic_details)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic details updated successfully.')
            return redirect('academic_details')  # Redirect to the academic details page

    else:
        form = AcademicDetailsForm(instance=academic_details)

    return render(request, 'applicants/academic_details_update.html', {'form': form})

def create_relevant_course(request):
    user = request.user

    if request.method == 'POST':
        form = RelevantCourseForm(request.POST)
        if form.is_valid():
            relevant_course = form.save(commit=False)
            relevant_course.user = user
            relevant_course.save()
            messages.success(request, 'Relevant course added successfully.')
            return redirect('relevant_courses')
    else:
        form = RelevantCourseForm()

    relevant_courses = RelevantCourse.objects.filter(user=user)

    context = {
        'form': form,
        'relevant_courses': relevant_courses
    }

    return render(request, 'applicants/relevant_course.html', context)

def update_relevant_course(request, relevant_course_id):
    user = request.user
    try:
        relevant_course = RelevantCourse.objects.get(id=relevant_course_id, user=user)
    except RelevantCourse.DoesNotExist:
        messages.error(request, 'Relevant course not found.')
        return redirect('relevant_courses')

    if request.method == 'POST':
        form = RelevantCourseForm(request.POST, instance=relevant_course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relevant course updated successfully.')
            return redirect('relevant_courses')
    else:
        form = RelevantCourseForm(instance=relevant_course)

    context = {
        'form': form,
        'relevant_course': relevant_course
    }

    return render(request, 'applicants/update_relevant_course.html', context)

def create_employment_history(request):
    user = request.user

    if request.method == 'POST':
        form = EmploymentHistoryForm(request.POST)
        if form.is_valid():
            employment_history = form.save(commit=False)
            employment_history.user = user
            employment_history.save()
            messages.success(request, 'Employment History added successfully.')
            return redirect('employment_history')
    else:
        form = EmploymentHistoryForm()

    employment_histories = EmploymentHistory.objects.filter(user=user)

    context = {
        'form': form,
        'employment_histories': employment_histories
    }

    return render(request, 'applicants/employment_history.html', context)

def update_employment_history(request, employment_history_id):
    employment_history = get_object_or_404(EmploymentHistory, id=employment_history_id)

    if request.method == 'POST':
        form = EmploymentHistoryForm(request.POST, instance=employment_history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employment History updated successfully.')
            return redirect('employment_history')
    else:
        form = EmploymentHistoryForm(instance=employment_history)

    context = {
        'form': form,
        'employment_history': employment_history
    }

    return render(request, 'applicants/update_employment_history.html', context)

def create_referee(request):
    user = request.user

    if request.method == 'POST':
        form = RefereeForm(request.POST)
        if form.is_valid():
            referee = form.save(commit=False)
            referee.user = user
            referee.save()
            messages.success(request, 'Referee added successfully.')
            return redirect('referee')
    else:
        form = RefereeForm()

    referees = Referee.objects.filter(user=user)  # Retrieve referee objects for the current user

    context = {
        'form': form,
        'referee': referees
    }

    return render(request, 'applicants/referee.html', context)

def save_resume(request):
    # Retrieve relevant data from other models
    academic_details = AcademicDetails.objects.filter(user=request.user)
    relevant_courses = RelevantCourse.objects.filter(user=request.user)
    employment_histories = EmploymentHistory.objects.filter(user=request.user)
    referees = Referee.objects.filter(user=request.user)

    # Check if a Resume instance already exists for the user
    resume, created = Resume.objects.get_or_create(user=request.user)

    # Populate the resume with data from other models
    if academic_details:
        for academic_detail in academic_details:
            resume.academic_details.add(academic_detail)
    
    if relevant_courses:
        for relevant_course in relevant_courses:
            resume.relevant_courses.add(relevant_course)
    
    if employment_histories:
        for employment_history in employment_histories:
            resume.employment_histories.add(employment_history)
    
    if referees:
        for referee in referees:
            resume.referees.add(referee)

    # Save the resume instance
    resume.save()
    messages.success(request, 'Your Resume Submitted successfully.')
    return redirect('index')


def apply_job(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    user = request.user

    if JobApplication.objects.filter(user=user, vacancy=vacancy).exists():
        messages.error(request, "You have already applied for this job.")
        return redirect('index')

    # Check if the applicant meets the qualifications
    try:
        academic_details = AcademicDetails.objects.get(user=user)
        academic_level = academic_details.academic_level
        specialization = academic_details.specialization
        area_of_study = academic_details.area_of_study
    except AcademicDetails.DoesNotExist:
        academic_level = None
        specialization = None
        area_of_study = None

    if academic_level == vacancy.academic_level and specialization == vacancy.specialization and area_of_study == vacancy.area_of_study:
        is_qualified = True
    else:
        is_qualified = False

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.vacancy = vacancy
            application.is_qualified = is_qualified  # Set the qualification status
            application.save()
            #send mail on succesful application
            mail_subject = 'Application succesful for {vacancy.job_name}'
            message = f"Thank you for showing interest to join our organization, we will have a look at you application and notify you on the status of your application."
            # to_email = payer['email_address']  # Use the payer's email address
            to_email = request.user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, "Job application submitted successfully.")
            return redirect('index')
    else:
        form = JobApplicationForm()

    return render(request, 'applicants/job_application.html', {'form': form, 'vacancy': vacancy})

def export_resume_to_excel(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return HttpResponse("Resume not found", status=404)

    resume_resource = ResumeResource()
    dataset = resume_resource.export(queryset=Resume.objects.filter(id=resume_id))
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume_id}_export.xls"'
    return response
