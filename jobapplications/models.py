from django.db import models
from ace.constants import CATEGORY_CHOICES, MAX_LENGTH_STANDARDFIELDS, MAX_LENGTH_STANDARDTEXTAREA, MAX_LENGTH_LONGSTANDARDFIELDS
from joblistings.models import Job
from accounts.models import Candidate, User
from tinymce import models as tinymce_models

# Create your models here.

class JobApplication(models.Model):

    firstName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")
    lastName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")
    preferredName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")
    #studentID = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS,  default= "")
    #category = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "Any", choices= CATEGORY_CHOICES)
    #location = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default= "")
    #skillList = models.CharField(max_length = MAX_LENGTH_LONGSTANDARDFIELDS,  default= "")
    #aboutYou = tinymce_models.HTMLField(max_length = MAX_LENGTH_STANDARDTEXTAREA, default= "")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, default= "")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.title + ' - ' + self.candidate.email

class Education(models.Model):
    institute = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    title = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    period = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    description = tinymce_models.HTMLField(max_length = MAX_LENGTH_STANDARDTEXTAREA, default= "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    JobApplication = models.ManyToManyField(JobApplication)

class Experience(models.Model):
    companyName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    title = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    period = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    description = tinymce_models.HTMLField(max_length = MAX_LENGTH_STANDARDTEXTAREA, default= "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    JobApplication = models.ManyToManyField(JobApplication)

class Resume(models.Model):
    fileName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    resume = models.FileField(upload_to='user/resume/', default= "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    JobApplication = models.ManyToManyField(JobApplication)

class SupportingDocument(models.Model):
    fileName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    document = models.FileField(upload_to='user/document/', default= "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    JobApplication = models.ManyToManyField(JobApplication)

class CoverLetter(models.Model):
    fileName = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    coverLetter = models.FileField(upload_to='user/coverletter/', default= "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    JobApplication = models.ManyToManyField(JobApplication)

    

