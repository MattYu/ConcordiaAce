#from django.views import ListView
from django.shortcuts import render, get_object_or_404

from joblistings.models import Job
from joblistings.forms import JobForm

# Create your views here.

def job_details(request, pk=None, *args, **kwargs):
    instance = get_object_or_404(Job, pk=pk)
    context = {
        'object': instance
    }
    return render(request, "job-details.html", context)

def post_job(request,  *args, **kwargs):

    if (request.method == "POST"):
        print(request.POST)

    context = {'form' : JobForm()}

    return render(request, "employer-dashboard-post-job.html", context)