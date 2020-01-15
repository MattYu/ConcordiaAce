from django import forms
from ace.constants import MAX_LENGTH_STANDARDFIELDS, MAX_LENGTH_LONGSTANDARDFIELDS
from accounts.models import User 
from companies.models import Company

class RegistrationForm(forms.Form):
    registrationType = forms.IntegerField(widget=forms.HiddenInput())
    employerCompany = forms.IntegerField(widget=forms.HiddenInput())

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
        companyType = kwargs.pop('companyType', None)
        super().__init__(*args, **kwargs)


        self.fields['registrationType'].initial =registrationType
        self.fields['employerCompany'].initial =companyType

        if (registrationType == "employer"):
            if (companyType == 'createNew'):
                self.fields['address'] = forms.CharField(max_length = 100, default= "")
                self.fields['website'] = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company address'}))
                self.fields['profile'] = forms.TextField(max_length = 1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company description'}))
                self.fields['image'] =   forms.ImageField(required=False, upload_to='images/company/', default="images/company/company-logo-1")
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
        if self.fields['employerCompany'].initial != 'Create':
            return True
        return False

    def isAllFieldSelected(self)-> bool:
        if self.fields['registrationType'].initial != 'employer' and self.fields['registrationType'].initial != 'candidate':
            return False
        if self.fields['registrationType'].initial == 'employer':
            if self.fields['employerCompany'].initial != 'Select' and self.fields['employerCompany'].initial != 'Create':
                return False
        return True