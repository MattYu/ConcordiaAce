from django.shortcuts import render, get_object_or_404
from joblistings.models import Job
from jobapplications.forms import ApplicationForm

count = 1
# Create your views here.
def add_resume(request, *args, **kwargs):
    #instance = get_object_or_404(Job, pk=pk)
    global count 
    if (request.method == 'POST'):
        if(request.POST.get('addEdu')):
            count +=1
            form = ApplicationForm(request.POST, extra_edu_count=count)

        if form.is_valid():
            pass
    else:
        count = 1
        form = ApplicationForm(extra_edu_count=count)
    return render(request, "add-resume.html", {'form': form})