from django import forms
from joblistings.models import Job
from ace.constants import CATEGORY_CHOICES, MAX_LENGTH_TITLE, MAX_LENGTH_DESCRIPTION, MAX_LENGTH_RESPONSABILITIES, MAX_LENGTH_REQUIREMENTS, MAX_LENGTH_STANDARDFIELDS, LOCATION_CHOICES
from tinymce.widgets import TinyMCE
from companies.models import Company
from joblistings.models import Job, JobPDFDescription
from django.shortcuts import get_object_or_404


class JobForm(forms.Form):
    title = forms.CharField(max_length=MAX_LENGTH_TITLE,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your job title here'})
                            )

    category = forms.ChoiceField(
        choices = CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Category'})
    )

    salaryRange = forms.CharField( 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salary range'})
    )

    vacancy = forms.IntegerField( 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vacancy'})
    )

    expirationDate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    startDate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    duration = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total duration in months'})
    )

    description = forms.CharField(
        max_length=MAX_LENGTH_DESCRIPTION,
        widget=TinyMCE(attrs={'class': 'tinymce-editor tinymce-editor-1'})
    )

    responsabilities = forms.CharField(
        max_length=MAX_LENGTH_RESPONSABILITIES,
        widget=TinyMCE(attrs={'class': 'tinymce-editor tinymce-editor-2'})
    )

    requirements = forms.CharField(
        max_length=MAX_LENGTH_REQUIREMENTS,
        widget=TinyMCE(attrs={'class': 'tinymce-editor tinymce-editor-2'})
    )

    country = forms.ChoiceField(
        choices = LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Country'})
    )

    location = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )

    postcode = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )

    yourLocation = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your location'})
    )

    company = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Category'})
    )

    descriptionFile = forms.FileField(required=False)

    class Meta:
        model = Job
        exclude = ('company',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        company = Company.objects.all()
        company_choices = []
        for obj in company:
            company_choices.append((obj.pk, obj))
        self.fields['company'].choices = company_choices

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        category = cleaned_data.get('category')
        salaryRange = cleaned_data.get('salaryRange')
        vacancy = cleaned_data.get('vacancy')
        expirationDate = cleaned_data.get('expirationDate')
        startDate = cleaned_data.get('startDate')
        duration = cleaned_data.get('duration')
        description = cleaned_data.get('description')
        responsabilities = cleaned_data.get('responsabilities')
        requirements = cleaned_data.get('requirements')
        country = cleaned_data.get('country')
        location = cleaned_data.get('location')
        postcode = cleaned_data.get('postcode')
        yourLocation = cleaned_data.get('yourLocation')
        company = cleaned_data.get('company')

        self.cleaned_data = cleaned_data

        if not title and not location and not salaryRange and not description and not location and not postcode:
            raise forms.ValidationError('You have to write something')
        '''
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
        '''

    def save(self):
        job = Job()
        cleaned_data = self.cleaned_data
        job.title = cleaned_data.get('title')
        job.category = cleaned_data.get('category')
        job.salaryRange = cleaned_data.get('salaryRange')
        job.vacancy = cleaned_data.get('vacancy')
        job.expirationDate = cleaned_data.get('expirationDate')
        job.startDate = cleaned_data.get('startDate')
        job.duration = cleaned_data.get('duration')
        job.description = cleaned_data.get('description')
        job.responsabilities = cleaned_data.get('responsabilities')
        job.requirements = cleaned_data.get('requirements')
        job.country = cleaned_data.get('country')
        job.location = cleaned_data.get('location')
        job.postcode = cleaned_data.get('postcode')
        job.yourLocation = cleaned_data.get('yourLocation')
        job.company = get_object_or_404(Company, pk=cleaned_data.get('company'))
        job.save()

        if cleaned_data.get('descriptionFile'):
            jobPDFDescription = JobPDFDescription()
            jobPDFDescription.job = job
            jobPDFDescription.descriptionFile = cleaned_data.get('descriptionFile')
            jobPDFDescription.save()


        return job
    