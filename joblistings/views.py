#from django.views import ListView
from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect



from joblistings.models import Job
from joblistings.forms import JobForm
from companies.models import Company

# Create your views here.

def job_details(request, pk=None, *args, **kwargs):
    instance = get_object_or_404(Job, pk=pk)
    context = {
        'object': instance
    }
    return render(request, "job-details.html", context)

def post_job(request,  *args, **kwargs):
    if (request.method == "POST"):
        form = JobForm(request.POST)
        if form.is_valid():
            form.clean()
            job = form.save()

            job_pk = job.pk
        

            return HttpResponseRedirect('/job-details/' + str(job_pk))

        
        print(request.POST)
    jobForm = JobForm()
    context = {'form' : jobForm}

    return render(request, "employer-dashboard-post-job.html", context)