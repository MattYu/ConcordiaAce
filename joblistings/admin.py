from django.contrib import admin

from .models import Job, JobPDFDescription

# Register your models here.
admin.site.register(Job)
admin.site.register(JobPDFDescription)