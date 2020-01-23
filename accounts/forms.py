from django import forms
from ace.constants import MAX_LENGTH_STANDARDFIELDS, MAX_LENGTH_LONGSTANDARDFIELDS, USER_TYPE_CANDIDATE, USER_TYPE_EMPLOYER
from accounts.models import Candidate, Employer, PreferredName, MyUserManager
from accounts.models import User
from companies.models import Company
from tinymce.widgets import TinyMCE
from django.shortcuts import get_object_or_404

class RegistrationForm(forms.Form):
    registrationType = forms.CharField(widget=forms.HiddenInput())
    employerCompany = forms.CharField(widget=forms.HiddenInput())

    email = forms.EmailField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
                                )

    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    passwordConfirm = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    firstName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
                                )

    lastName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
                                )
    
    preferredName = forms.CharField(required=False, max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred First Name (optional)'})
                                )

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        registrationType = kwargs.pop('registrationType', None)
        companyType = kwargs.pop('employerCompany', None)
        super().__init__(*args, **kwargs)

        print(User.objects.all())
        self.fields['registrationType'].initial =registrationType
        self.fields['employerCompany'].initial =companyType
        print(companyType)

        if (registrationType == "employer"):
            if (companyType == 'createNew'):
                self.fields['companyName'] = forms.CharField(max_length = 100,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}))
                self.fields['address'] = forms.CharField(max_length = 100,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company address'}))
                self.fields['website'] = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company website'}))
                self.fields['profile'] = forms.CharField(
                                                            max_length=1000,
                                                            widget=TinyMCE(attrs={'class': 'tinymce-editor tinymce-editor-2'})
                                                        )
                self.fields['image'] =   forms.ImageField(required=False)
            if (companyType == 'selectFromExisting'):
                self.fields['company'] = forms.ChoiceField(
                                                            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Category'})
                                                        )
                company = Company.objects.all()
                company_choices = []
                for obj in company:
                    company_choices.append((obj.pk, obj))
                self.fields['company'].choices = company_choices

    def is_type_selected(self)-> bool:
        if self.fields['registrationType'].initial == 'employer' or self.fields['registrationType'].initial == 'candidate':
            return True
        return False

    def is_employer_selected(self)-> bool:
        if self.fields['registrationType'].initial == 'employer':
            return True
        return False

    def is_candidate_selected(self)-> bool:
        if self.fields['registrationType'].initial == 'candidate':
            return True
        return False
    
    def is_createCompany_selected(self)-> bool:
        if self.fields['employerCompany'].initial == 'createNew':
            return True
        return False

    def isAllFieldSelected(self)-> bool:
        if self.fields['registrationType'].initial != 'employer' and self.fields['registrationType'].initial != 'candidate':
            return False
        if self.fields['registrationType'].initial == 'employer':
            if self.fields['employerCompany'].initial != 'selectFromExisting' and self.fields['employerCompany'].initial != 'createNew':
                return False
        return True

    def clean(self):
        cleaned_data = super().clean()
        User.objects.all()
        if self.is_createCompany_selected() and self.is_createCompany_selected():
            if not cleaned_data.get('image'):
                raise forms.ValidationError('You have to upload a logo for your company')

        if cleaned_data.get('password') != cleaned_data.get('passwordConfirm'):
            raise forms.ValidationError('Passwords do not match')
        if User.objects.filter(email=cleaned_data.get('email')).count() != 0:
            raise forms.ValidationError('Email is already in use')


        self.cleaned_data = cleaned_data

    def save(self):
        self.clean()
        cleaned_data = self.cleaned_data
        userManager = MyUserManager()
        email = cleaned_data.get('email')
        firstName = cleaned_data.get('firstName')
        lastName = cleaned_data.get('lastName')
        user_type = None
        if self.is_employer_selected():
            user_type = USER_TYPE_EMPLOYER
        else:
            user_type = USER_TYPE_CANDIDATE
        password = cleaned_data.get('password')
        print(user_type)

        
        user = User()
        user.email = email
        user.firstName = firstName
        user.lastName = lastName
        user.user_type = user_type


        user.set_password(password)
        user.save()
        
        if cleaned_data.get('preferredName') != '' and cleaned_data.get('preferredName') !=None:
            preferredName = PreferredName()
            preferredName.user = user
            preferredName.preferredName = cleaned_data.get('preferredName')
            preferredName.save()

        if self.is_employer_selected:
            employer = Employer()
            employer.user = user

            if self.is_createCompany_selected():
                company = Company()
                print('!!!!!!!!!!!!!!!!!!!test!!!!!!!!!!!!!!!')
                company.name = cleaned_data.get('companyName')
                company.address = cleaned_data.get('address')
                company.website = cleaned_data.get('website')
                company.profile = cleaned_data.get('profile')
                company.image = cleaned_data.get('image')
                company.save()
                employer.company = company

            else:
                print('!!!!!!!!!!!!!!!!!!!here!!!!!!!!!!!!!!!')
                employer.company = get_object_or_404(Company, pk=cleaned_data.get('company'))
                print(employer.company)
        else:
            candidate = Candidate()
            candidate.user =user

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=MAX_LENGTH_STANDARDFIELDS,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
                            )

    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))