#from django.views import ListView
from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q


from ace.constants import USER_TYPE_CANDIDATE, USER_TYPE_EMPLOYER
from joblistings.models import Job, JobPDFDescription, JobAccessPermission
from joblistings.forms import JobForm
from companies.models import Company
from accounts.models import Employer
from django_sendfile import sendfile



# Create your views here.
def job_search(request, *args, **kwargs):
    if request.method == 'POST':
        keywords = request.POST['keyword']
        location = request.POST['search-location']

        args = []
        queries = keywords.split(" ")
        for query in queries:
            q1 = Q(company__name__icontains=query)
            q2 = Q(description__icontains=query)
            q3 = Q(title__icontains=query)
            q4 = Q(responsabilities__icontains=query)
            combined_q = q1 | q2 | q3 | q4
            args.append(combined_q)

        qs = Job.objects.filter(*args).distinct()
        qs = list(set(qs))

        queryset = []
        for q in qs:
            if q.location.lower() == location or q.country.lower() == location:
                queryset.append(q)
 
        context = {
            'joblist': queryset
        }

        return render(request, 'joblist_view.html', context)

    return HttpResponseRedirect("/")


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

    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please register with ACE first"
        return HttpResponseRedirect('/login')
    else:
        if request.user.user_type == USER_TYPE_CANDIDATE:
            request.session['info'] = "You are logged in as a candidate. Only employers can access this page"
            return  HttpResponseRedirect('/')

    if (request.method == "POST"):
        form = JobForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.clean()
            job = form.save()

            if request.user.user_type == USER_TYPE_EMPLOYER:
                jobAccessPermission = JobAccessPermission()
                jobAccessPermission.job = job
                jobAccessPermission.save()
                jobAccessPermission.employer.add(Employer.objects.get(user=request.user))
                

            job_pk = job.pk
            
            

            return HttpResponseRedirect('/job-details/' + str(job_pk))

        
        print(request.POST)
    jobForm = JobForm()
    context = {'form' : jobForm}

    return render(request, "employer-dashboard-post-job.html", context)

def download_jobPDF(request, pk):
    download = get_object_or_404(JobPDFDescription, job=pk)
    return sendfile(request, download.descriptionFile.path)

