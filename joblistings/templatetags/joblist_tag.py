from django import template
from joblistings.models import Job
from companies.models import Company


register = template.Library()

@register.inclusion_tag('joblist_view.html')
def get_joblist(*args, **kwargs):
    queryset = None
    origin = kwargs["origin"]
    if (origin == "main_page"):
        queryset = Job.objects.all()[:10]

    return {
        'joblist': queryset
    }