from django.db import models
from companies.models import Company

MAX_LENGTH_TITLE = 120
MAX_LENGTH_DESCRIPTION = 1000
MAX_LENGTH_RESPONSABILITIES = 600
MAX_LENGTH_REQUIREMENTS = 600
MAX_LENGTH_STANDARDFIELDS= 30

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length = MAX_LENGTH_TITLE)
    
    #Job Summary
    category = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    location = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "Montreal")
    jobtype = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    salaryRange = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "N/A")
    expirationDate = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")


    description = models.TextField(max_length = MAX_LENGTH_DESCRIPTION, default= "")
    responsabilities = models.TextField(max_length = MAX_LENGTH_RESPONSABILITIES, default= "")
    requirements = models.TextField(max_length = MAX_LENGTH_REQUIREMENTS, default= "")

    # Job Location
    country = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    city = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "Montreal")
    postcode = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")
    yourLocation = models.CharField(max_length = MAX_LENGTH_STANDARDFIELDS, default= "")

    company = models.ForeignKey(Company, on_delete=models.CASCADE, default= "")

    def __str__(self):
        return self.title

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in Job._meta.fields]

#class Company(models.Model):



