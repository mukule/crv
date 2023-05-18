from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import DateInput
from django.forms import ModelForm, DateInput
from .models import *



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'ID NUMBER', 'class': 'form-control'}),
        label='',
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label='',
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'class': 'form-control'}),
        label='',
       
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'class': 'form-control'}),
        label='',
        
    )
 

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'autocomplete': 'new-password'}),
        
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'autocomplete': 'new-password'}),
        
    )


    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    phone = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS_CHOICES, required=False)
    postal_address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image', 'phone', 'date_of_birth', 'gender', 'marital_status', 'postal_address']

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)


class AcademicDetailsForm(ModelForm):
    institution_name = forms.CharField(max_length=100)
    admission_number = forms.CharField(max_length=20)
    start_year = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    end_year = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    graduation_year = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AcademicDetails
        fields = ['academic_level', 'area_of_study', 'specialization', 'examining_body',
                  'institution_name', 'admission_number', 'start_year', 'end_year', 'graduation_year']
        
class RelevantCourseForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    completion_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model = RelevantCourse
        fields = ['course_name', 'institution', 'certification', 'start_date', 'completion_date']

class EmploymentHistoryForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model = EmploymentHistory
        fields = ['company_name', 'position', 'position_description', 'start_date', 'end_date']

class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ['name', 'organization', 'occupation', 'relationship_period', 'email', 'phone']
       