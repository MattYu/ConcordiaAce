from django import template
from ..models import Job

register = template.Library()

@register.inclusion_tag('joblist_view.html', takes_context=True)
def get_joblist(context):
    queryset = Job.objects.all()
    print("test*****************")
    print(queryset)
    for job in queryset:
        print(job)
        
    return {
        'joblist': queryset
    }