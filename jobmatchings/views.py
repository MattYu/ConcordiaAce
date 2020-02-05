from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from jobapplications.models import JobApplication, Ranking
from django.db.models import Q
from joblistings.models import Job
from ace.constants import USER_TYPE_CANDIDATE, USER_TYPE_EMPLOYER, USER_TYPE_SUPER
from accounts.models import Employer, Candidate
from jobmatchings.forms import EmployerRankingForm, CandidateRankingForm

from jobmatchings.models import MatchingHistory, Match
from matching import games as ranking
from django.db import transaction

# Create your views here.
@transaction.atomic
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

@transaction.atomic
def candidate_view_rankings(request):
    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login first"
        return HttpResponseRedirect('/login')


    if request.user.user_type == USER_TYPE_CANDIDATE:

        if (request.method == "POST"):
            print(request.POST)
            for rank in Ranking.objects.filter(candidate__id=Candidate.objects.get(user=request.user).id, is_closed=False).all():
                print(request.POST)
                if request.POST.get(str(rank.id)):
                    print(request.POST)
                    rank.candidateRank = int(request.POST.get(str(rank.id)))
                    rank.save()

        form = CandidateRankingForm(candidateId=Candidate.objects.get(user=request.user).id)

        context = {
            "form" : form,
            }

    return render(request, "dashboard-ranking-candidate.html", context)

@transaction.atomic
def admin_matchmaking(request):
    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login first"
        return HttpResponseRedirect('/login')


    if request.user.user_type == USER_TYPE_SUPER:

        if (request.method == "POST"):
            print(request.POST)

            if request.POST.get("closeEmp"):

                for rank in Ranking.objects.filter(is_ranking_open_for_employer=True):
                    rank.is_ranking_open_for_employer = False
                    rank.is_ranking_open_for_candidate = True
                    rank.save()

            if request.POST.get("closeCan"):
                for rank in Ranking.objects.filter(is_ranking_open_for_candidate=True):
                    rank.is_ranking_open_for_candidate = False
                    rank.save()

            if request.POST.get("MATCH"):
                matchingHistory = MatchingHistory()
                matchingHistory.save()

                for rank in Ranking.objects.filter(is_closed=False):
                    if rank.candidateRank == 1000 or rank.candidateRank == 999 or rank.employerRank == 1000 or rank.employerRank == 9:
                        rank.status = "Not Matched"
                        rank.jobApplication.status = "Not Matched"
                        rank.is_closed = True
                        rank.save()

                    if rank.candidateRank == 1 and rank.employerRank == 1 and rank.jobApplication.job.vacancy !=0:
                        rank.jobApplication.job.vacancy -= 1
                        match = Match()
                        match.candidate = rank.candidate
                        match.job = rank.jobApplication.job
                        match.jobApplication = rank.jobApplication

                        match.save()

                        rank.status = "Matched"
                        rank.jobApplication.status = "Matched"

                        matchingHistory.matches.add(match)
                        matchingHistory.save()

                        rank.is_closed = True
                        rank.save()


                employer_prefs = {}
                capacities = {}

                for rank in Ranking.objects.filter(is_closed=False).order_by('employerRank'):
                    jobApplication = rank.jobApplication.id

                    if jobApplication not in employer_prefs:
                        employer_prefs[jobApplication] = [rank.candidate.id]
                        capacities[jobApplication] = JobApplication.objects.get(id=jobApplication).job.vacancy
                    else:
                        employer_prefs[jobApplication].append(rank.candidate.id)
                
                candidate_prefs = {}
                for rank in Ranking.objects.filter(is_closed=False).order_by('candidateRank'):
                    candidate = rank.candidate.id

                    if candidate not in candidate_prefs:
                        candidate_prefs[candidate] = [rank.jobApplication.id]
                    else:
                        candidate_prefs[candidate].append(rank.jobApplication.id)


                match = ranking.HospitalResident.create_from_dictionaries( candidate_prefs, employer_prefs, capacities)

                matchResult = match.solve(optimal="hospital")

                for jobApplication in matchResult:
                    for candidate in matchResult[jobApplication]:
                        match = Match()
                        match.candidate = Candidate.objects.get(id=int(candidate.name))
                        match.job = JobApplication.objects.get(id=int(jobApplication.name)).job
                        match.jobApplication = JobApplication.objects.get(id=int(jobApplication.name))
                        match.save()

                        jobApp = JobApplication.objects.get(id=int(jobApplication.name))
                        jobApp.status = "Matched"
                        jobApp.save()

                        matchingHistory.matches.add(match)
                        matchingHistory.save()

                for rank in Ranking.objects.filter(is_closed=False):
                    if Match.objects.filter(jobApplication=rank.jobApplication).count() == 0:
                        rank.status = "Not Matched"
                        rank.jobApplication.status = "Not Matched"
                        rank.save()
                    else:
                        rank.status = "Matched"
                        rank.jobApplication.status = "Matched"
                        rank.save()

        context = {
            "user": request.user
            }

    return render(request, "dashboard-ranking-matchday.html", context)



def view_matching(request, jobId= None):
    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login first"
        return HttpResponseRedirect('/login')


    if request.user.user_type == USER_TYPE_SUPER:

        if jobId == None:
        
            jobQuery = Job.objects.all()

            jobs = []


            for job in jobQuery:
                obj = {}

                obj['job'] = job
                obj['count'] = Match.objects.filter(job=job).count()
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


            matches = Match.objects.filter(job__id=jobId)

            context["matches"] = matches

    if request.user.user_type == USER_TYPE_EMPLOYER:

        if jobId == None:
            jobQuery = Job.objects.filter(jobAccessPermission = Employer.objects.get(user=request.user))


            jobs = []
            for job in jobQuery:
                obj = {}
                obj['job'] = job
                obj['count'] = Match.objects.filter(job=job).count()
                jobs.append(obj)

            context = {
                        "jobs" : jobs,
                        'user' : request.user,
                        }
        else:
            jobQuery = get_object_or_404(Job, id=jobId, jobAccessPermission = Employer.objects.get(user=request.user))


            context = {
                        "job" : jobQuery,
                        }

            matches = Match.objects.filer(job__id=jobId)

            context["matches"] = matches


    if request.user.user_type == USER_TYPE_CANDIDATE:

        matches = Match.objects.filer(candidate=Candidate.objects.get(user=request.user))

        context = {
                    "job": True,
                    "matches" : matches,
                    }       

    return render(request, "dashboard-match.html", context)