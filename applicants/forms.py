from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import DateInput
from django.forms import ModelForm, DateInput
from .models import *
from multiupload.fields import MultiFileField
from ckeditor.widgets import CKEditorWidget


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'ID NUMBER', 'class': 'form-control'}),
        label='',
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label='',
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter First Name', 'class': 'form-control'}),
        label='',
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Last Name', 'class': 'form-control'}),
        label='',
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'autocomplete': 'new-password'}),
    )

    INTEREST_CHOICES = (
        ('I', 'Internship'),
        ('E', 'Employment'),
    )
    interest = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Select your interest'}),
        label='',
        required=True,
    )

    DISABILITY_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    is_person_with_disability = forms.ChoiceField(
        choices=DISABILITY_CHOICES,
        widget=forms.Select(attrs={
                            'class': 'form-control', 'placeholder': 'Are you a person with a disability?'}),
        label='',
        required=False,
    )
    pwd_no = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'PWD Number', 'class': 'form-control'}),
        label='',
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2', 'interest', 'is_person_with_disability', 'pwd_no']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.interest = self.cleaned_data['interest']
        user.is_person_with_disability = self.cleaned_data['is_person_with_disability']
        user.pwd_no = self.cleaned_data['pwd_no']
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
    date_of_birth = forms.DateField(
        required=False, widget=DateInput(attrs={'type': 'date'}))
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
    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS_CHOICES, required=False)
    postal_address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image', 'phone',
                  'date_of_birth', 'gender', 'marital_status', 'postal_address']


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)


class AcademicDetailsForm(forms.ModelForm):
    institution_name = forms.CharField(max_length=100)
    admission_number = forms.CharField(max_length=20)
    start_year = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    end_year = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=False)
    graduation_year = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = AcademicDetails
        fields = ['academic_level', 'area_of_study', 'specialization', 'examining_body',
                  'institution_name', 'admission_number', 'start_year', 'end_year', 'graduation_year', 'is_studying']

    def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')
        graduation_year = cleaned_data.get('graduation_year')

        if start_year and end_year and start_year > end_year:
            self.add_error(
                'start_year', "Start year cannot be greater than end year.")

        if end_year and graduation_year and end_year > graduation_year:
            self.add_error(
                'end_year', "End year cannot be greater than graduation year.")

        present_date = timezone.now().date()

        if end_year and end_year > present_date:
            self.add_error(
                'end_year', "End year cannot be greater than the present date.")

        if graduation_year and graduation_year > present_date:
            self.add_error(
                'graduation_year', "Graduation year cannot be greater than the present date.")


class RelevantCourseForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    completion_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = RelevantCourse
        fields = ['course_name', 'institution', 'certification',
                  'start_date', 'completion_date', 'is_studying']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        completion_date = cleaned_data.get('completion_date')
        is_studying = cleaned_data.get('is_studying')

        if start_date and completion_date and start_date > completion_date:
            self.add_error(
                'start_date', "Start date cannot be greater than completion date.")

        present_date = timezone.now().date()

        if start_date and start_date > present_date:
            self.add_error('start_date', "Start date cannot be a future date.")

        if completion_date and completion_date > present_date:
            self.add_error(
                'completion_date', "Completion date cannot be greater than the present date.")

        if not completion_date and not is_studying:
            self.add_error(
                None, "Provide a completion date or indicate if still studying.")

        if completion_date and is_studying:
            self.add_error(
                None, "Provide either a completion date or indicate if still studying, not both.")

        return cleaned_data


class EmploymentHistoryForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = EmploymentHistory
        fields = ['company_name', 'position', 'position_description',
                  'start_date', 'end_date', 'currently_working_here']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        currently_working_here = cleaned_data.get('currently_working_here')

        if not end_date and not currently_working_here:
            self.add_error(
                'end_date', "Either an end date or 'currently working here' must be provided.")

        if end_date and currently_working_here:
            self.add_error('currently_working_here',
                           "You cannot be 'currently working here' and provide an end date.")

        if start_date and end_date and start_date > end_date:
            self.add_error(
                'start_date', "Start date cannot be greater than end date.")

        present_date = timezone.now().date()

        if start_date and start_date > present_date:
            self.add_error(
                'start_date', "Start date cannot be greater than the present date.")

        if end_date and end_date > present_date:
            self.add_error(
                'end_date', "End date cannot be greater than the present date.")


class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ['name', 'organization', 'occupation',
                  'relationship_period', 'email', 'phone']


class JobApplicationForm(forms.ModelForm):
    cover_letter = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = JobApplication
        fields = ['cover_letter']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(JobApplicationForm, self).__init__(*args, **kwargs)


class DocumentForm(forms.ModelForm):
    documents = MultiFileField(
        min_num=1, max_num=5, max_file_size=1024 * 1024 * 5)

    class Meta:
        model = Document
        fields = ['documents']


class JobSearchForm(forms.Form):
    keywords = forms.CharField(max_length=100, required=False)
    area_of_study = forms.ModelChoiceField(
        queryset=AreaOfStudy.objects.all(), required=False)
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(), required=False)
    vacancy_type = forms.ModelChoiceField(
        queryset=VacancyType.objects.all(), required=False)


class VacancyForm(forms.ModelForm):
    job_name = forms.CharField(
        max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_ref = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    reports_to = forms.CharField(
        max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    academic_level = forms.ModelChoiceField(queryset=AcademicLevel.objects.all(
    ), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    area_of_study = forms.ModelChoiceField(queryset=AreaOfStudy.objects.all(
    ), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(
    ), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    department = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number_of_vacancies = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    vacancy_type = forms.ModelChoiceField(queryset=VacancyType.objects.all(
    ), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    date_open = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    date_closed = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}), required=False)
    job_description = forms.CharField(
        widget=CKEditorWidget(attrs={'id': 'job_description', 'class': 'form-control'}))
    requirements = forms.CharField(
        widget=CKEditorWidget(attrs={'id': 'requirements', 'class': 'form-control'}))
    responsibilities = forms.CharField(
        widget=CKEditorWidget(attrs={'id': 'responsibilities', 'class': 'form-control'}))

    class Meta:
        model = Vacancy
        exclude = ['document', 'date_created', 'is_filled']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fields that are required
        required_fields = ['job_name', 'job_ref',
                           'academic_level', 'date_open']

        for field_name, field in self.fields.items():
            if field_name in required_fields:
                field.required = True
            else:
                field.required = False
