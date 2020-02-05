from django.db import models
from jobapplications.models import Ranking

from accounts.models import Candidate
from joblistings.models import Job

# Create your models here.
class Match(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, default= "")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default= "")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MatchingHistory(models.Model):

    matches = models.ManyToManyField(Match)

    open_matching_to_employer = models.BooleanField(default= True)
    open_matching_to_candidate = models.BooleanField(default= False)

    matchingInProgress = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




