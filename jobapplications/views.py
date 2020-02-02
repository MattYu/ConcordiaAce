from django.shortcuts import render, get_object_or_404
from joblistings.models import Job
from jobapplications.models import JobApplication
from jobapplications.forms import ApplicationForm, resumeUpload
from django_sendfile import sendfile
import uuid
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from ace.constants import USER_TYPE_EMPLOYER, USER_TYPE_CANDIDATE
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from io import BytesIO, StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader
import requests


#u = uuid.uuid4()
#u.hex

# Create your views here.
def add_resume(request, pk= None, *args, **kwargs):
    
    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login before applying to a job"
        return HttpResponseRedirect('/login')
    else:
        if request.user.user_type == USER_TYPE_EMPLOYER:
            request.session['info'] = "You are logged in as an employer. Only candidates can access this page"
            return  HttpResponseRedirect('/')
    
    instance = get_object_or_404(Job, pk=pk)
    context = {'job': instance}
    
    if (request.method == 'POST'):
        form = ApplicationForm(
            request.POST, 
            request.FILES,
            extra_edu_count=request.POST.get('extra_edu_count'), 
            extra_exp_count=request.POST.get('extra_exp_count'), 
            extra_doc_count=request.POST.get('extra_doc_count'), 
            )
        #request.session['form'] = form.as_p()
        if form.is_valid():
            form.clean()
            jobApplication = form.save(instance, request.user)

            return HttpResponseRedirect('/')
    else:
        form = ApplicationForm(extra_edu_count=1, extra_exp_count=1, extra_doc_count=0, user=request.user)
    context['form'] = form
    return render(request, "add-resume.html", context)


def download_test(request, pk):
    download = get_object_or_404(Job, pk=pk)
    return sendfile(request, download.company.image.path)


def browse_job_applications(request):
    context = {}

    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login before applying to a job"
        return HttpResponseRedirect('/login')


    if request.user.user_type == 4:
        
        jobApplications = JobApplication.objects.all()

        context = {"jobApplications" : jobApplications}
    

    return render(request, "dashboard-manage-applications.html", context)


def view_application_details(request, pk):
    context = {}

    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login before applying to a job"
        return HttpResponseRedirect('/login')

    if request.user.user_type == USER_TYPE_EMPLOYER:

        jobsWithPermission = Job.objects.filter(JobAccessPermission__employer=request.user)
        jobApplications.objects.filter(job=jobsWithPermission)

    if request.user.user_type == USER_TYPE_CANDIDATE:
        jobApplications.objects.filter(candidate=request.user)


    return render(request, "dashboard-manage-applications.html")


def concatinate_applicationPDF(request):

    manager = PoolManager(10)
    

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=form.pdf'

    getFile = requests.get("http://127.0.0.1:8000/jobDescription/1/").content

        
    writer = PdfFileWriter()
    memoryFile = BytesIO(getFile)

    
    pdfFile = PdfFileReader(memoryFile)

    for pageNum in range(pdfFile.getNumPages()):
        currentPage = pdfFile.getPage(pageNum)
        #currentPage.mergePage(watermark.getPage(0))
        writer.addPage(currentPage)

    getFile = requests.get("http://127.0.0.1:8000/jobDescription/1/").content

    pdfFile = PdfFileReader(memoryFile)

    for pageNum in range(pdfFile.getNumPages()):
        currentPage = pdfFile.getPage(pageNum)
        #currentPage.mergePage(watermark.getPage(0))
        writer.addPage(currentPage)
    #pdf11 = pdf1.render()
    #http_response = HttpResponse(pdf11, content_type='application/pdf')
    #http_response['Content-Disposition'] = 'filename="report.pdf"'
    outputStream = BytesIO()
    writer.write(outputStream)
    response.write(outputStream.getvalue())
    return response
    