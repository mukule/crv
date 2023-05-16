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
from .forms import SetPasswordForm,PasswordResetForm, AcademicDetailsForm
from django.db.models.query_utils import Q
from .models import AcademicDetails
from django.contrib.auth import get_user_model

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


def update_academic_details(request):
    user = request.user
    academic_details, created = AcademicDetails.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = AcademicDetailsForm(request.POST, instance=academic_details)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page

    else:
        form = AcademicDetailsForm(instance=academic_details)

    return render(request, 'applicants/academic_details.html', {'form': form})