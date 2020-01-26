from django.contrib import admin

from .models import Job, JobPDFDescription, JobAccessPermission

# Register your models here.
admin.site.register(Job)
admin.site.register(JobPDFDescription)
admin.site.register(JobAccessPermission)