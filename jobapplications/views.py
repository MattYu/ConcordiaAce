from django.shortcuts import render, get_object_or_404
from joblistings.models import Job
from jobapplications.forms import ApplicationForm

count = 1
# Create your views here.
def add_resume(request, *args, **kwargs):
    #instance = get_object_or_404(Job, pk=pk)
    global count 
    if (request.method == 'POST'):
        print(request.POST)
        if(request.POST.get('addEdu')):
            form = ApplicationForm(request.POST, extra_edu_count=request.POST.get('extra_edu_count'))

        if form.is_valid():
            pass
    else:
        form = ApplicationForm(extra_edu_count=1)
    return render(request, "add-resume.html", {'form': form})