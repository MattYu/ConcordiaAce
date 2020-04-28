from django.shortcuts import render, get_object_or_404
from companies.models import Company
from companies.forms import AdminMigrateCompany
from ace.constants import USER_TYPE_SUPER
from joblistings.models import Job
from django.db.models import Q
from accounts.models import Employer
from django.http import HttpResponse
# Create your views here.

def view_company_details(request, pk):
    instance = get_object_or_404(Company, pk=pk)
    jobs = Job.objects.filter((Q(status="Approved") | Q(status="Interviewing"))).order_by('created_at').distinct()
    context = {
        'company': instance,
        'pk': pk,
        'jobs':jobs,
        "jobsLen": len(jobs)
    }
    if request.user.is_authenticated and request.user.user_type == USER_TYPE_SUPER:
        if request.method == 'POST':
            if request.POST.get('Not Approved'):
                instance.status = "Not Approved"
                instance.save()
            if request.POST.get('Approved'):
                instance.status = "Approved"
                instance.save()
            if request.POST.get('Migrate'):
                if request.POST.get("validCompany") != "Approved Companies" and request.POST.get("employer") != "Company's employees":
                    employer = get_object_or_404(Employer, pk=int(request.POST.get("employer")))
                    employer.company = int(request.POST.get("validCompany"))
                    employer.save()

        form = AdminMigrateCompany(pk=pk)
        context["form"] = form

    return render(request, "employer-details.html", context)


def manage_companies(request):
    if request.user.is_authenticated and request.user.user_type == USER_TYPE_SUPER:
        filterquery = Q()
        companies = Company.objects.filter(filterquery).order_by('-created_at').all()
        
        context = {
            "companies": companies,
        }

        return render(request, "dashboard-manage-company.html", context)

    else:
        return HttpResponse('Invalid permission')