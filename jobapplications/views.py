from django.shortcuts import render, get_object_or_404
from joblistings.models import Job
from jobapplications.forms import ApplicationForm, resumeUpload
from django_sendfile import sendfile
import uuid
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

#u = uuid.uuid4()
#u.hex

# Create your views here.
def add_resume(request, pk= None, *args, **kwargs):
    instance = get_object_or_404(Job, pk=pk)
    context = {'job': instance}
    
    if (request.method == 'POST'):
        form = ApplicationForm(
            request.POST, 
            request.FILES,
            extra_edu_count=request.POST.get('extra_edu_count'), 
            extra_exp_count=request.POST.get('extra_exp_count'), 
            extra_doc_count=request.POST.get('extra_doc_count')
            )
        #request.session['form'] = form.as_p()
        if form.is_valid():
            form.clean()
            form.save(instance)
            return HttpResponseRedirect('')
    else:
        form = ApplicationForm(extra_edu_count=1, extra_exp_count=1, extra_doc_count=0)
    context['form'] = form
    return render(request, "add-resume.html", context)


def download_test(request, pk):
    download = get_object_or_404(Job, pk=pk)
    return sendfile(request, download.company.image.path)