from django.shortcuts import render, get_object_or_404
from joblistings.models import Job
from jobapplications.models import JobApplication, Resume, CoverLetter
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

from ace.constants import FILE_TYPE_RESUME, FILE_TYPE_COVER_LETTER, FILE_TYPE_TRANSCRIPT, FILE_TYPE_OTHER, USER_TYPE_SUPER, USER_TYPE_CANDIDATE, USER_TYPE_EMPLOYER

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django_sendfile import sendfile
from accounts.models import downloadProtectedFile_token, User, Candidate
import uuid
from django.db import transaction

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

@transaction.atomic
def browse_job_applications(request):
    context = {}
    jobApplications = None

    if not request.user.is_authenticated:

        request.session['redirect'] = request.path
        request.session['warning'] = "Warning: Please login before applying to a job"
        return HttpResponseRedirect('/login')


    if request.user.user_type == USER_TYPE_SUPER:
        
        jobApplications = JobApplication.objects.all()

        context = {"jobApplications" : jobApplications}

    if request.user.user_type == USER_TYPE_EMPLOYER:

        jobApplications = JobApplication.objects.filter(job__permission__employer__user__id = request.user.id)
    
    if (request.method == 'POST'):
    #if request.POST.get("pdf"):
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=downloadApplications.pdf'
        writer = PdfFileWriter()
        # Change to https in prod (although django should automatically force https if settings.py is configured corretly in prod)
        base_url = "http://" + str(get_current_site(request).domain)  + "/getFile"
    
        User.objects.filter(id=request.user.id).update(protect_file_temp_download_key=str(uuid.uuid4().hex))
        token = downloadProtectedFile_token.make_token(request.user)

        for application in jobApplications:
            uid = urlsafe_base64_encode(force_bytes(request.user.pk))
            candidateId = urlsafe_base64_encode(force_bytes(application.pk))


            fileId = Resume.objects.get(JobApplication=application).id
            fileId = urlsafe_base64_encode(force_bytes(fileId))
            fileType =  urlsafe_base64_encode(force_bytes(FILE_TYPE_RESUME))

            url = base_url + "/" + str(uid) + "/" + str(candidateId) + "/"+ str(fileType) + "/" + str(fileId) + "/" + str(token) + "/"
            getFile = requests.get(url).content
            memoryFile = BytesIO(getFile)
            pdfFile = PdfFileReader(memoryFile)
  
            for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                #currentPage.mergePage(watermark.getPage(0))
                writer.addPage(currentPage)

            fileId = CoverLetter.objects.get(JobApplication=application).id
            fileId = urlsafe_base64_encode(force_bytes(fileId))
            fileType =  urlsafe_base64_encode(force_bytes(FILE_TYPE_COVER_LETTER))

            url = base_url + "/" + str(uid) + "/" + str(candidateId) + "/"+ str(fileType) + "/" + str(fileId) + "/" + str(token) + "/"
            getFile = requests.get(url).content
            memoryFile = BytesIO(getFile)
            pdfFile = PdfFileReader(memoryFile)

            for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                #currentPage.mergePage(watermark.getPage(0))
                writer.addPage(currentPage)


            fileType =  urlsafe_base64_encode(force_bytes(FILE_TYPE_TRANSCRIPT))

            url = base_url + "/" + str(uid) + "/" + str(candidateId) + "/"+ str(fileType) + "/" + str(fileId) + "/" + str(token) + "/"
            getFile = requests.get(url).content
            memoryFile = BytesIO(getFile)
            pdfFile = PdfFileReader(memoryFile)

            for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                #currentPage.mergePage(watermark.getPage(0))
                writer.addPage(currentPage)
        
        outputStream = BytesIO()
        writer.write(outputStream)
        response.write(outputStream.getvalue())

        User.objects.filter(id=request.user.id).update(protect_file_temp_download_key="")

        return response

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
    
def get_protected_file(request, uid, candidateId, filetype, fileid, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and downloadProtectedFile_token.check_token(user, token):

        fileType = force_text(urlsafe_base64_decode(filetype))
        fileId = force_text(urlsafe_base64_decode(fileid))
        candidateId = force_text(urlsafe_base64_decode(candidateId))

        if fileType == str(FILE_TYPE_RESUME):
            resume = Resume.objects.get(id=fileId).resume
            filePath = resume.path


        if fileType == str(FILE_TYPE_COVER_LETTER):
            coverLetter = CoverLetter.objects.get(id=fileId).coverLetter
            filePath = coverLetter.path
 

        if fileType == str(FILE_TYPE_TRANSCRIPT):
            transcript = Candidate.objects.get(id=candidateId).transcript
            filePath = transcript.path

        if fileType == str(FILE_TYPE_OTHER):
            filePath = None

        return sendfile(request, filePath)
    else:
        return HttpResponse('Invalid permission token')

