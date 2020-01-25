#from django.views import ListView
from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect



from joblistings.models import Job, JobPDFDescription
from joblistings.forms import JobForm
from companies.models import Company
from django_sendfile import sendfile

# Create your views here.

def job_details(request, pk=None, *args, **kwargs):
    instance = get_object_or_404(Job, pk=pk)

    context = {
        'object': instance,
        'pk': pk
    }

    jobPDF = JobPDFDescription.objects.filter(job=pk)

    if (jobPDF):
        context["download"] = pk

    return render(request, "job-details.html", context)

def post_job(request,  *args, **kwargs):
    if (request.method == "POST"):
        form = JobForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.clean()
            job = form.save()

            job_pk = job.pk
            
            

            return HttpResponseRedirect('/job-details/' + str(job_pk))

        
        print(request.POST)
    jobForm = JobForm()
    context = {'form' : jobForm}

    return render(request, "employer-dashboard-post-job.html", context)

def download_jobPDF(request, pk):
    download = get_object_or_404(JobPDFDescription, job=pk)
    return sendfile(request, download.descriptionFile.path)