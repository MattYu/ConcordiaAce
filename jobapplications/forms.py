from django import forms
from ace.constants import CATEGORY_CHOICES, MAX_LENGTH_STANDARDFIELDS, MAX_LENGTH_LONGSTANDARDFIELDS
from jobapplications.models import JobApplication, Education, Experience, Resume, SupportingDocument, CoverLetter
from tinymce.widgets import TinyMCE
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404
from joblistings.models import Job
import uuid

class resumeUpload(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('resume',)

class documentUpload(forms.ModelForm):
    class Meta:
        model = SupportingDocument
        fields = ('document',)

class documentUpload(forms.ModelForm):
    class Meta:
        model = CoverLetter
        fields = ('coverLetter',)

class ApplicationForm(forms.Form):

    numberOfEduForms = 1
    numberOfCVForm = 1
    numberOfCoverLetterForm = 1

    extra_edu_count = forms.IntegerField(widget=forms.HiddenInput())
    extra_exp_count = forms.IntegerField(widget=forms.HiddenInput())
    extra_doc_count = forms.IntegerField(widget=forms.HiddenInput())


    firstName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
                                )

    lastName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
                                )
    
    preferredName = forms.CharField(max_length=MAX_LENGTH_STANDARDFIELDS,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred First Name (optional)'})
                                )


    #resume = resumeUpload()
    resume = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'add-new-field'}))
    #coverLetter = documentUpload()
    coverLetter = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'add-new-field'}))

    class Meta:
        model = JobApplication

    def __init__(self, *args, **kwargs):
        extra_edu_fields = kwargs.pop('extra_edu_count', 1)
        extra_exp_fields = kwargs.pop('extra_exp_count', 1)
        extra_doc_fields = kwargs.pop('extra_doc_count', 0)
        super().__init__(*args, **kwargs)
    

        self.fields['extra_edu_count'].initial = max(min(int(extra_edu_fields), 10),1)
        self.educationFields = []
        self.educationFieldsNames = []
        for i in range(int(self.fields['extra_edu_count'].initial)):
            field_name = '_educations_%s' % (i,)
            educationDict = {}
            eduNameDict = {}
            self.fields['institute' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_STANDARDFIELDS,
                                                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institute'})
                                                                    )
            educationDict['institute'] = self['institute' + field_name]
            eduNameDict['institute'] = 'institute' + field_name
            self.fields['title' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_STANDARDFIELDS,
                                                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Degree'})
                                                                )
            educationDict['title'] = self['title' + field_name]
            eduNameDict['title'] = 'title' + field_name
            self.fields['period' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_STANDARDFIELDS,
                                                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Period'})
                                                                )
            educationDict['period'] = self['period' + field_name]
            eduNameDict['period'] = 'period' + field_name
            self.fields['description' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_LONGSTANDARDFIELDS,
                                                                        required= False,
                                                                        widget=TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Description (Optional)'})
                                                                    )
            educationDict['description'] = self['description' + field_name]
            eduNameDict['description'] = 'description' + field_name
            
            self.educationFields.append(educationDict)
            self.educationFieldsNames.append(eduNameDict)


        self.fields['extra_exp_count'].initial = max(min(int(extra_exp_fields), 10),1)
        self.experienceFields = [] 
        self.experienceFieldsNames = []
        for i in range(int(self.fields['extra_exp_count'].initial)):
            field_name = '_experience_%s' % (i,)
            experienceDict = {}
            expNameDict = {}
            self.fields['companyName' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_STANDARDFIELDS,
                                                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'})
                                                                    )
            experienceDict['companyName'] = self['companyName' + field_name]
            expNameDict['companyName'] = 'companyName' + field_name
            self.fields['title' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_STANDARDFIELDS,
                                                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title'})
                                                                )
            experienceDict['title'] = self['title' + field_name]
            expNameDict['title'] = 'title' + field_name
            self.fields['period' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_STANDARDFIELDS,
                                                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Period'})
                                                                )
            experienceDict['period'] = self['period' + field_name]
            expNameDict['period'] = 'period' + field_name
            self.fields['description' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_LONGSTANDARDFIELDS,
                                                                        required= False,
                                                                        widget=TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Description (Optional)'})
                                                                    )
            experienceDict['description'] = self['description' + field_name]
            expNameDict['description'] = 'description' + field_name

            self.experienceFields.append(experienceDict)
            self.experienceFieldsNames.append(expNameDict)


        resume = forms.FileField()

        
        self.fields['extra_doc_count'].initial = max(min(int(extra_doc_fields), 10), 0)
        self.documentsFields = []
        self.documentsFieldsNames = []
        for i in range(int(self.fields['extra_doc_count'].initial)):
            field_name = '_doc_%s' % (i,)
            docDict = {}
            docName = {}
            self.fields['name' + field_name] = forms.CharField(
                                                                        max_length=MAX_LENGTH_STANDARDFIELDS,
                                                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supporting document name / type'})
                                                                    )
            docDict['name'] = self['name' + field_name]
            docName['name'] = 'name' + field_name
            self.fields['file' + field_name] = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'add-new-field'}))
            docDict['file'] = self['file' + field_name]
            docName['file'] = 'file' + field_name
           
            self.documentsFields.append(docDict)
            self.documentsFieldsNames.append(docName)

    def get_education_fields(self):
        return self.educationFields

    def get_experience_fields(self):
        return self.experienceFields

    def get_document_fields(self):
        return self.documentsFields

    def clean(self):
        cleaned_data = super().clean()

        self.cleaned_data = cleaned_data

    def save(self, pk):

        jobApplication = JobApplication()
        cleaned_data = self.cleaned_data
        jobApplication.firstName = cleaned_data.get('firstName')
        jobApplication.lastName = cleaned_data.get('lastName')
        jobApplication.preferredName = cleaned_data.get('preferredName')
        jobApplication.job = get_object_or_404(Job, pk=pk.pk)
        jobApplication.save()

        resume = Resume()
        resume.fileName = cleaned_data.get('resume').name
        resume.resume.upload_to = 'protected/application/' + pk.title + '/resume/' + uuid.uuid4().hex  + '/'
        resume.resume = cleaned_data.get('resume')
        resume.save()
        resume.JobApplication.add(jobApplication)
        resume.save()

        coverLetter = CoverLetter()
        coverLetter.fileName = cleaned_data.get('coverLetter').name
        coverLetter.coverLetter.upload_to = 'protected/application/' + pk.title + '/coverletter/' + uuid.uuid4().hex + '/'
        coverLetter.coverLetter = cleaned_data.get('coverLetter')
        coverLetter.save()
        coverLetter.JobApplication.add(jobApplication)
        coverLetter.save()


        for edu in self.educationFieldsNames:
            education = Education()
            education.institute = cleaned_data.get(edu['institute'])
            education.title = cleaned_data.get(edu['title'])
            education.period = cleaned_data.get(edu['period'])
            education.description = cleaned_data.get(edu['description'])
            education.save()
            education.JobApplication.add(jobApplication)
            education.save()

        for exp in self.experienceFieldsNames:
            experience = Experience()
            experience.companyName = cleaned_data.get(exp['companyName'])
            experience.title = cleaned_data.get(exp['title'])
            experience.period = cleaned_data.get(exp['period'])
            experience.description = cleaned_data.get(exp['description'])
            experience.save()
            experience.JobApplication.add(jobApplication)
            experience.save()

        for doc in self.documentsFieldsNames:
            document = SupportingDocument()
            document.fileName = cleaned_data.get(doc['name'])
            document.document.upload_to  = 'protected/application/' + pk.title + '/supportingDocument/' + uuid.uuid4().hex  + '/'
            document.document = cleaned_data.get(doc['file'])
            document.save()



        '''
        firstName
        lastName
        preferredName
        '''