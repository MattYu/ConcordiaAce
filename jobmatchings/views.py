from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from jobapplications.models import JobApplication
from django.db.models import Q
from joblistings.models import Job
from ace.constants import USER_TYPE_CANDIDATE, USER_TYPE_EMPLOYER, USER_TYPE_SUPER
from accounts.models import Employer, Candidate

# Create your views here.
def employer_view_rankings(request, jobId= None):
    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login first"
        return HttpResponseRedirect('/login')


    if request.user.user_type == USER_TYPE_SUPER:
        
        jobQuery = Job.objects.all()

        jobs = {}

        jobs = []

        query1 = Q(status="Interviewing")
        query2 = Q(status="Not Approved")

        for job in jobQuery:
            obj = {}

            obj['job'] = job
            obj['count'] = JobApplication.objects.filter(job=job).count()
            jobs.append(obj)

        context = {
                    "jobs" : jobs,
                    'user' : request.user,
                }

    if request.user.user_type == USER_TYPE_EMPLOYER:

        jobQuery = Job.objects.filter(jobAccessPermission = Employer.objects.get(user=request.user))

        query1 = ~Q(status="Pending Review")
        query2 = ~Q(status="Not Approved")


        jobs = []
        for job in jobQuery:
            obj = {}

            obj['job'] = job

            obj['count'] = JobApplication.objects.filter(query1|query2,job=job).count()
            
            jobs.append(obj)


        context = {
                    "jobs" : jobs,
                    'user' : request.user,
                }

    if request.user.user_type == USER_TYPE_CANDIDATE:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: This page is only accessible to employers"
        return HttpResponseRedirect('/')

    return render(request, "dashboard-ranking.html", context)
