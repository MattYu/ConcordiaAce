from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from jobapplications.models import JobApplication, Ranking
from django.db.models import Q
from joblistings.models import Job
from ace.constants import USER_TYPE_CANDIDATE, USER_TYPE_EMPLOYER, USER_TYPE_SUPER
from accounts.models import Employer, Candidate
from jobmatchings.forms import EmployerRankingForm, CandidateRankingForm

# Create your views here.
def employer_view_rankings(request, jobId= None):
    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login first"
        return HttpResponseRedirect('/login')


    if request.user.user_type == USER_TYPE_SUPER:

        if jobId == None:
        
            jobQuery = Job.objects.all()

            jobs = {}

            jobs = []

            query1 = Q(status="Interviewing")
            query2 = Q(status="Ranked")
            query3 = Q(status="1st")

            for job in jobQuery:
                obj = {}

                obj['job'] = job
                obj['count'] = JobApplication.objects.filter(query1|query2|query3, job=job).count()
                jobs.append(obj)

            context = {
                        "jobs" : jobs,
                        'user' : request.user,
                    }

        else:
            jobQuery = get_object_or_404(Job, id=jobId)

            context = {
                        "job" : jobQuery,
                        }

            if (request.method == "POST"):
                for rank in Ranking.objects.filter(job__id=jobId).all():
                    if request.POST.get(str(rank.id)):
                        rank.employerRank = int(request.POST.get(str(rank.id)))
                        rank.save()


            form = EmployerRankingForm(jobId=jobId)

            context["form"] = form

    if request.user.user_type == USER_TYPE_EMPLOYER:

        if jobId == None:
            jobQuery = Job.objects.filter(jobAccessPermission = Employer.objects.get(user=request.user))

            query1 = Q(status="Interviewing")
            query2 = Q(status="Ranked")
            query3 = Q(status="1st")


            jobs = []
            for job in jobQuery:
                obj = {}

                obj['job'] = job

                obj['count'] = JobApplication.objects.filter(query1|query2|query3,job=job).count()
                
                jobs.append(obj)

            context = {
                        "jobs" : jobs,
                        'user' : request.user,
                        }
        else:
            jobQuery = get_object_or_404(Job, id=jobId, jobAccessPermission = Employer.objects.get(user=request.user))

            if (request.method == "POST"):
                for rank in Ranking.objects.filter(job__id=jobId).all():
                    if request.POST.get(str(rank.id)):
                        rank.employerRank = int(request.POST.get(str(rank.id)))
                        rank.save()

            context = {
                        "job" : jobQuery,
                        }

            form = EmployerRankingForm(jobId=jobId)

            context["form"] = form

    if request.user.user_type == USER_TYPE_CANDIDATE:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: This page is only accessible to employers"
        return HttpResponseRedirect('/')

    return render(request, "dashboard-ranking.html", context)


def candidate_view_rankings(request):
    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login first"
        return HttpResponseRedirect('/login')


    if request.user.user_type == USER_TYPE_CANDIDATE:

        form = CandidateRankingForm(candidateId=Candidate.objects.get(user=request.user).id)
        
        context = {
            "form" : form,
            }

    return render(request, "dashboard-ranking-candidate.html", context)
