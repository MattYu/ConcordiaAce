from django import template
from joblistings.models import Job
from companies.models import Company


register = template.Library()

@register.inclusion_tag('navbar.html')
def get_navbar(*args, **kwargs):
    queryset = None
    origin = kwargs["origin"]
    if (origin == "main_page"):
        queryset = Job.objects.order_by('-created_at')[:10]

    return {
        'joblist': queryset
    }