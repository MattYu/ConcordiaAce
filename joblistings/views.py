from django.views import ListView
from django.shortcuts import render

from .models import Job

# Create your views here.

def job_list_view(request):
    queryset = Job.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "")
