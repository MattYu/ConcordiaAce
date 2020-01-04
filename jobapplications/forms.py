from django import forms
from ace.constants import CATEGORY_CHOICES, MAX_LENGTH_STANDARDFIELDS
from jobapplications.models import JobApplication, Education

class ApplicationForm(forms.Form):

    numberOfEduForms = 1
    numberOfCVForm = 1
    numberOfCoverLetterForm = 1

    extra_edu_count = forms.IntegerField(widget=forms.HiddenInput())


    firstName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your given name'})
                                )

    lastName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your family name'})
                                )
    
    preferredName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your preferred given name [optional]'})
                                )
    

    category = forms.ChoiceField(
        choices = CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Category'})
    )

    class Meta:
        model = JobApplication

    def __init__(self, *args, **kwargs):
        extra_edu_fields = kwargs.pop('extra_edu_count', 1)
        super().__init__(*args, **kwargs)

        print(extra_edu_fields)
        self.fields['extra_edu_count'].initial = int(extra_edu_fields)
        
        for i in range(int(self.fields['extra_edu_count'].initial)):
            field_name = 'educations_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            self.initial[field_name] = ""
            count = i


    def get_education_fields(self):
        for field_name in self.fields:
            if field_name.startswith('educations_'):
                yield self[field_name]